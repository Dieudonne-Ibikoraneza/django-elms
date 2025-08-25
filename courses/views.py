from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.http import JsonResponse
from django.utils import timezone
from .models import Course, Enrollment, Lesson, LessonProgress
from .forms import CourseForm
from users.views import is_instructor
from notifications.models import Notification

class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Course.objects.filter(status='published').select_related('instructor', 'category')
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search) |
                Q(instructor__username__icontains=search)
            )
        
        # Category filter
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Level filter
        level = self.request.GET.get('level')
        if level:
            queryset = queryset.filter(level=level)
        
        # Sorting
        sort_by = self.request.GET.get('sort', '-created_at')
        if sort_by in ['title', '-title', 'price', '-price', 'created_at', '-created_at']:
            queryset = queryset.order_by(sort_by)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['levels'] = Course.LEVEL_CHOICES
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_level'] = self.request.GET.get('level', '')
        context['sort_by'] = self.request.GET.get('sort', '-created_at')
        return context

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        
        # Check if user is enrolled
        is_enrolled = False
        enrollment = None
        if self.request.user.is_authenticated:
            try:
                enrollment = Enrollment.objects.get(student=self.request.user, course=course)
                is_enrolled = True
            except Enrollment.DoesNotExist:
                pass
        
        context.update({
            'is_enrolled': is_enrolled,
            'enrollment': enrollment,
            'modules': course.modules.prefetch_related('lessons').all(),
            'reviews': course.reviews.select_related('student')[:10],
            'average_rating': course.average_rating,
            'discussions': course.discussions.select_related('author')[:5],
        })
        return context

@login_required
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk, status='published')
    
    # Check if already enrolled
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.warning(request, 'You are already enrolled in this course.')
        return redirect('courses:course_detail', pk=pk)
    
    # Check if course is full
    if course.max_students and course.enrollments.count() >= course.max_students:
        messages.error(request, 'This course is full.')
        return redirect('courses:course_detail', pk=pk)
    
    # Create enrollment
    enrollment = Enrollment.objects.create(student=request.user, course=course)
    
    # Create notification
    Notification.objects.create(
        user=request.user,
        notification_type='enrollment',
        title='Successfully Enrolled',
        message=f'You have been enrolled in "{course.title}"'
    )
    
    messages.success(request, f'Successfully enrolled in "{course.title}"!')
    return redirect('courses:course_learn', pk=pk)

@login_required
def course_learn(request, pk):
    """Course learning interface for enrolled students"""
    course = get_object_or_404(Course, pk=pk)
    
    # Check enrollment
    try:
        enrollment = Enrollment.objects.get(student=request.user, course=course)
    except Enrollment.DoesNotExist:
        messages.error(request, 'You are not enrolled in this course.')
        return redirect('courses:course_detail', pk=pk)
    
    # Get current lesson (first incomplete or first lesson)
    current_lesson = None
    completed_lessons = LessonProgress.objects.filter(
        enrollment=enrollment, completed=True
    ).values_list('lesson_id', flat=True)
    
    for module in course.modules.all():
        for lesson in module.lessons.all():
            if lesson.id not in completed_lessons:
                current_lesson = lesson
                break
        if current_lesson:
            break
    
    if not current_lesson and course.modules.exists():
        # All lessons completed, show first lesson
        current_lesson = course.modules.first().lessons.first()
    
    # Update progress
    enrollment.calculate_progress()
    
    context = {
        'course': course,
        'enrollment': enrollment,
        'current_lesson': current_lesson,
        'modules': course.modules.prefetch_related('lessons').all(),
        'completed_lessons': completed_lessons,
    }
    return render(request, 'courses/course_learn.html', context)

@login_required
def lesson_view(request, course_pk, lesson_pk):
    """Individual lesson view"""
    course = get_object_or_404(Course, pk=course_pk)
    lesson = get_object_or_404(Lesson, pk=lesson_pk, module__course=course)
    
    # Check enrollment or preview
    if not lesson.is_preview:
        try:
            enrollment = Enrollment.objects.get(student=request.user, course=course)
        except Enrollment.DoesNotExist:
            messages.error(request, 'You need to enroll to access this lesson.')
            return redirect('courses:course_detail', pk=course_pk)
    else:
        enrollment = None
    
    # Mark lesson as completed if POST request
    if request.method == 'POST' and enrollment:
        progress, created = LessonProgress.objects.get_or_create(
            enrollment=enrollment,
            lesson=lesson,
            defaults={'completed': True, 'completed_at': timezone.now()}
        )
        if not progress.completed:
            progress.completed = True
            progress.completed_at = timezone.now()
            progress.save()
        
        enrollment.calculate_progress()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'progress': enrollment.progress_percentage})
    
    context = {
        'course': course,
        'lesson': lesson,
        'enrollment': enrollment,
        'is_completed': enrollment and LessonProgress.objects.filter(
            enrollment=enrollment, lesson=lesson, completed=True
        ).exists() if enrollment else False,
    }
    return render(request, 'courses/lesson_detail.html', context)

@user_passes_test(is_instructor)
def instructor_courses(request):
    """Instructor's course management"""
    courses = Course.objects.filter(instructor=request.user).annotate(
        student_count=Count('enrollments')
    )
    return render(request, 'courses/instructor/course_list.html', {'courses': courses})

@user_passes_test(is_instructor)
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('courses:instructor_courses')
    else:
        form = CourseForm()
    return render(request, 'courses/instructor/course_form.html', {'form': form, 'title': 'Create Course'})