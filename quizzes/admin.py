from django.contrib import admin
from .models import Quiz, Question, Answer, QuizAttempt, StudentAnswer

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'lesson', 'passing_score', 'max_attempts', 'created_at']
    list_filter = ['course', 'lesson', 'created_at']
    search_fields = ['title', 'description', 'course__title']
    raw_id_fields = ['course', 'lesson']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'quiz', 'question_type', 'points', 'order']
    list_filter = ['question_type', 'quiz__course']
    search_fields = ['question_text', 'quiz__title']
    raw_id_fields = ['quiz']
    list_editable = ['order']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['answer_text', 'question', 'is_correct', 'order']
    list_filter = ['is_correct', 'question__quiz']
    search_fields = ['answer_text', 'question__question_text']
    raw_id_fields = ['question']
    list_editable = ['is_correct', 'order']

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['student', 'quiz', 'score', 'passed', 'started_at', 'completed_at']
    list_filter = ['passed', 'started_at', 'quiz__course']
    search_fields = ['student__username', 'quiz__title']
    raw_id_fields = ['student', 'quiz']
    date_hierarchy = 'started_at'

@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'is_correct', 'points_earned']
    list_filter = ['is_correct', 'attempt__quiz']
    search_fields = ['question__question_text', 'attempt__student__username']
    raw_id_fields = ['attempt', 'question', 'selected_answer']