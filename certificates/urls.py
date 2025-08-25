from django.urls import path
from . import views

app_name = 'certificates'

urlpatterns = [
    path('<int:enrollment_pk>/', views.generate_certificate, name='generate_certificate'),
]