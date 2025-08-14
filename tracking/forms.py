import re
from django import forms

ALNUM_ONLY = re.compile(r"[^A-Za-z0-9]+")

def sanitize_tracking(value: str) -> str:
    if not value:
        return ""
    cleaned = ALNUM_ONLY.sub("", value).strip().upper()
    return cleaned

class TrackingForm(forms.Form):
    tracking = forms.CharField(
        label="Tracking Number",
        widget=forms.TextInput(attrs={
            "placeholder": "Scan or type tracking number",
            "autofocus": "autofocus",
            "inputmode": "numeric",
            "autocomplete": "off",
        }),
        max_length=255,
    )

    def clean_tracking(self):
        raw = self.cleaned_data["tracking"]
        cleaned = sanitize_tracking(raw)
        if not cleaned:
            raise forms.ValidationError("Please enter digits (letters/spaces are removed).")
        return cleaned
