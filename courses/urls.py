from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list'),
    path('<uuid:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('<uuid:pk>/enroll/', views.enroll_course, name='enroll_course'),
    path('<uuid:pk>/learn/', views.course_learn, name='course_learn'),
    path('<uuid:course_pk>/lesson/<int:lesson_pk>/', views.lesson_view, name='lesson_view'),
    path('instructor/courses/', views.instructor_courses, name='instructor_courses'),
    path('instructor/courses/create/', views.create_course, name='create_course'),
]