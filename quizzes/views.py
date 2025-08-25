from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import Quiz, QuizAttempt, StudentAnswer, Answer
from .forms import QuizForm
from courses.models import Course, Enrollment
from notifications.models import Notification

@login_required
def quiz_take(request, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    if not Enrollment.objects.filter(student=request.user, course=quiz.course).exists():
        messages.error(request, 'You need to enroll in the course to take this quiz.')
        return redirect('courses:course_detail', pk=quiz.course.pk)
    
    # Check attempt limit
    attempts = QuizAttempt.objects.filter(student=request.user, quiz=quiz).count()
    if attempts >= quiz.max_attempts:
        messages.error(request, 'You have reached the maximum number of attempts.')
        return redirect('courses:course_detail', pk=quiz.course.pk)
    
    if request.method == 'POST':
        attempt = QuizAttempt.objects.create(student=request.user, quiz=quiz)
        total_points = 0
        max_points = sum(q.points for q in quiz.questions.all())
        
        for question in quiz.questions.all():
            answer_key = f'question_{question.id}'
            if answer_key in request.POST:
                if question.question_type in ['multiple_choice', 'true_false']:
                    selected_answer_id = request.POST.get(answer_key)
                    selected_answer = Answer.objects.get(id=selected_answer_id)
                    is_correct = selected_answer.is_correct
                    points_earned = question.points if is_correct else 0
                else:  # short_answer
                    text_answer = request.POST.get(answer_key)
                    is_correct = False  # Requires manual grading
                    points_earned = 0
                
                StudentAnswer.objects.create(
                    attempt=attempt,
                    question=question,
                    selected_answer=selected_answer if question.question_type in ['multiple_choice', 'true_false'] else None,
                    text_answer=text_answer if question.question_type == 'short_answer' else '',
                    is_correct=is_correct,
                    points_earned=points_earned
                )
                total_points += points_earned
        
        attempt.score = (total_points / max_points) * 100 if max_points > 0 else 0
        attempt.passed = attempt.score >= quiz.passing_score
        attempt.completed_at = timezone.now()
        attempt.save()
        
        Notification.objects.create(
            user=request.user,
            notification_type='quiz_graded',
            title=f'Quiz "{quiz.title}" Graded',
            message=f'You scored {attempt.score}% on {quiz.title}'
        )
        
        messages.success(request, f'Quiz submitted! Your score: {attempt.score}%')
        return redirect('courses:course_learn', pk=quiz.course.pk)
    
    context = {
        'quiz': quiz,
        'questions': quiz.questions.prefetch_related('answers').all(),
        'attempt_number': attempts + 1,
    }
    return render(request, 'quizzes/quiz_take.html', context)