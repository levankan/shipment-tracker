from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import TrackingForm
from .models import EmailRecipient, TrackingSubmission

def is_warehouse(user):
    return (
        user.is_authenticated and
        (user.is_superuser or user.groups.filter(name="warehouse_employee").exists())
    )


@user_passes_test(is_warehouse)
def submit_tracking(request):
    if request.method == "POST":
        form = TrackingForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data["tracking"]
            raw = request.POST.get("tracking", cleaned)

            # Save log
            TrackingSubmission.objects.create(
                raw_input=raw,
                cleaned_tracking=cleaned,
                submitted_by=request.user if request.user.is_authenticated else None,
            )

            # Build recipient list
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
