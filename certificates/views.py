from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.template.loader import render_to_string
from weasyprint import HTML
from django.core.files.base import ContentFile
from .models import Certificate
from courses.models import Enrollment

@login_required
def generate_certificate(request, enrollment_pk):
    enrollment = get_object_or_404(Enrollment, pk=enrollment_pk, student=request.user)
    if enrollment.progress_percentage < 100:
        messages.error(request, 'You must complete the course to generate a certificate.')
        return redirect('courses:course_learn', pk=enrollment.course.pk)
    
    certificate, created = Certificate.objects.get_or_create(enrollment=enrollment)
    if created:
        html_string = render_to_string('certificates/certificate_template.html', {
            'student': enrollment.student,
            'course': enrollment.course,
            'certificate_id': certificate.certificate_id,
            'issued_at': certificate.issued_at,
        })
        pdf_file = HTML(string=html_string).write_pdf()
        certificate.pdf_file.save(f'certificate_{certificate.certificate_id}.pdf', ContentFile(pdf_file))
        certificate.save()
        enrollment.certificate_issued = True
        enrollment.save()
    
    return HttpResponse(certificate.pdf_file, content_type='application/pdf')