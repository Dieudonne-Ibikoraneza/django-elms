from django.contrib import admin
from .models import Certificate

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['certificate_id', 'enrollment', 'issued_at']
    list_filter = ['issued_at']
    search_fields = ['certificate_id', 'enrollment__student__username', 'enrollment__course__title']
    raw_id_fields = ['enrollment']
    date_hierarchy = 'issued_at'