from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from .forms import CustomUserCreationForm, ProfileUpdateForm
from courses.models import Course, Enrollment

# Helper functions for role checking
def is_admin(user):
    return user.role == 'admin'

def is_instructor(user):
    return user.role in ['admin', 'instructor']

def is_student(user):
    return user.role == 'student'

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('users:dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def dashboard_view(request):
    user = request.user
    context = {'user': user}
    
    if user.role == 'admin':
        context.update({
            'total_users': User.objects.count(),
            'total_courses': Course.objects.count(),
            'total_enrollments': Enrollment.objects.count(),
            'recent_enrollments': Enrollment.objects.select_related('student', 'course')[:10]
        })
        return render(request, 'users/dashboard/admin_dashboard.html', context)
    
    elif user.role == 'instructor':
        courses = Course.objects.filter(instructor=user)
        context.update({
            'my_courses': courses,
            'total_students': Enrollment.objects.filter(course__instructor=user).count(),
            'total_courses': courses.count(),
        })
        return render(request, 'users/dashboard/instructor_dashboard.html', context)
    
    else:  # student
        enrollments = Enrollment.objects.filter(student=user).select_related('course')
        context.update({
            'my_enrollments': enrollments,
            'completed_courses': enrollments.filter(completed_at__isnull=False),
            'in_progress_courses': enrollments.filter(completed_at__isnull=True),
        })
        return render(request, 'users/dashboard/student_dashboard.html', context)

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})