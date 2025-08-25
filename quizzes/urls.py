from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    path('<int:quiz_pk>/take/', views.quiz_take, name='quiz_take'),
]