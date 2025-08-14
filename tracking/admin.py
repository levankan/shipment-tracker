from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import EmailRecipient, TrackingSubmission

@admin.register(EmailRecipient)
class EmailRecipientAdmin(admin.ModelAdmin):
    list_display = ("email", "active")
    list_filter = ("active",)
    search_fields = ("email",)

@admin.register(TrackingSubmission)
class TrackingSubmissionAdmin(admin.ModelAdmin):
    list_display = ("cleaned_tracking", "submitted_by", "submitted_at")
    search_fields = ("cleaned_tracking", "raw_input")
    list_filter = ("submitted_at",)
