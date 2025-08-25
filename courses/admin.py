from django.contrib import admin
from .models import Category, Course, Module, Lesson, Enrollment, LessonProgress, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'category', 'status', 'level', 'price', 'created_at']
    list_filter = ['status', 'category', 'level', 'created_at']
    search_fields = ['title', 'description', 'instructor__username']
    list_editable = ['status']
    raw_id_fields = ['instructor', 'category']
    date_hierarchy = 'created_at'

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'created_at']
    list_filter = ['course', 'created_at']
    search_fields = ['title', 'course__title']
    raw_id_fields = ['course']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'lesson_type', 'order', 'is_preview', 'created_at']
    list_filter = ['lesson_type', 'is_preview', 'module__course', 'created_at']
    search_fields = ['title', 'module__title', 'module__course__title']
    raw_id_fields = ['module']
    list_editable = ['is_preview']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrolled_at', 'progress_percentage', 'certificate_issued']
    list_filter = ['enrolled_at', 'certificate_issued', 'course']
    search_fields = ['student__username', 'course__title']
    raw_id_fields = ['student', 'course']
    date_hierarchy = 'enrolled_at'

@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'lesson', 'completed', 'completed_at']
    list_filter = ['completed', 'completed_at', 'enrollment__course']
    search_fields = ['enrollment__student__username', 'lesson__title']
    raw_id_fields = ['enrollment', 'lesson']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['course', 'student', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'course']
    search_fields = ['course__title', 'student__username', 'review_text']
    raw_id_fields = ['course', 'student']