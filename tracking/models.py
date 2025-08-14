from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models

class EmailRecipient(models.Model):
    email = models.EmailField(unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.email} ({'active' if self.active else 'inactive'})"


class TrackingSubmission(models.Model):
    raw_input = models.CharField(max_length=255)
    cleaned_tracking = models.CharField(max_length=255, db_index=True)
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cleaned_tracking} @ {self.submitted_at:%Y-%m-%d %H:%M}"
