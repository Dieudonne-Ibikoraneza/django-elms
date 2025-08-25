from django.db import models
import uuid
from courses.models import Enrollment

class Certificate(models.Model):
    """Course completion certificates"""
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE)
    certificate_id = models.UUIDField(default=uuid.uuid4, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='certificates/', blank=True, null=True)
    
    def __str__(self):
        return f"Certificate - {self.enrollment.student.username} - {self.enrollment.course.title}"