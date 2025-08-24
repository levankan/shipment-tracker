from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import TrackingForm
from .models import EmailRecipient, TrackingSubmission


def is_warehouse(user):
    """Allow superusers or users in the 'warehouse_employee' group."""
    return user.is_authenticated and (
        user.is_superuser or user.groups.filter(name="warehouse_employee").exists()
    )


@login_required(login_url="login")                 # force login
@user_passes_test(is_warehouse, login_url="login") # legacy-compatible
def submit_tracking(request):
    # For logged-in users who fail the group test, return 403 (prevent loops)
    if not is_warehouse(request.user):
        raise PermissionDenied

    if request.method == "POST":
        form = TrackingForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data["tracking"]
            raw = request.POST.get("tracking", cleaned)

            # Save log
            TrackingSubmission.objects.create(
                raw_input=raw,
                cleaned_tracking=cleaned,
                submitted_by=request.user,
            )

            # Recipients
            recipients = list(
                EmailRecipient.objects.filter(active=True).values_list("email", flat=True)
            )
            if recipients:
                subject = f"Tracking: {cleaned}"
                body = f"Tracking number submitted: {cleaned}"
                send_mail(subject, body, None, recipients, fail_silently=False)
                messages.success(request, f"Sent to {len(recipients)} recipient(s).")
            else:
                messages.warning(request, "No active recipients configured by admin.")

            return redirect(reverse("tracking:submit"))
    else:
        form = TrackingForm()

    return render(request, "tracking/submit.html", {"form": form})
