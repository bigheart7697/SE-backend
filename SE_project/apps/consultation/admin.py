from django.contrib import admin
from .models import ConsultationRequest


@admin.register(ConsultationRequest)
class RequestAdmin(admin.ModelAdmin):
    model = ConsultationRequest
