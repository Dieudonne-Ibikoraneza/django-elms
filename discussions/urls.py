from django.urls import path
from . import views

app_name = 'discussions'

urlpatterns = [
    path('courses/<uuid:course_pk>/discussions/', views.discussion_list, name='discussion_list'),
    path('courses/<uuid:course_pk>/discussions/<int:discussion_pk>/', views.discussion_detail, name='discussion_detail'),
]