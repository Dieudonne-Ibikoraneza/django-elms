from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Discussion
from .forms import DiscussionForm, ReplyForm
from courses.models import Course

@login_required
def discussion_list(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    discussions = course.discussions.select_related('author').prefetch_related('replies')
    return render(request, 'discussions/discussion_list.html', {'course': course, 'discussions': discussions})

@login_required
def discussion_detail(request, course_pk, discussion_pk):
    discussion = get_object_or_404(Discussion, pk=discussion_pk, course__pk=course_pk)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            Reply.objects.create(
                discussion=discussion,
                author=request.user,
                content=form.cleaned_data['content']
            )
            messages.success(request, 'Reply posted successfully!')
            return redirect('discussions:discussion_detail', course_pk=course_pk, discussion_pk=discussion_pk)
    else:
        form = ReplyForm()
    
    context = {
        'course': discussion.course,
        'discussion': discussion,
        'replies': discussion.replies.select_related('author').all(),
        'form': form,
    }
    return render(request, 'discussions/discussion_detail.html', context)