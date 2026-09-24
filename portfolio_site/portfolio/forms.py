from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    # Honeypot — real visitors leave this empty; bots usually fill it.
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "hp-field",
            "tabindex": "-1",
            "autocomplete": "off",
            "aria-hidden": "true",
        }),
    )

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Your name",
                "class": "field-input",
                "autocomplete": "name",
                "maxlength": "100",
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "Email",
                "class": "field-input",
                "autocomplete": "email",
                "maxlength": "254",
            }),
            "phone": forms.TextInput(attrs={
                "placeholder": "Phone (optional)",
                "class": "field-input",
                "autocomplete": "tel",
                "maxlength": "20",
            }),
            "subject": forms.TextInput(attrs={
                "placeholder": "Subject",
                "class": "field-input",
                "maxlength": "150",
            }),
            "message": forms.Textarea(attrs={
                "placeholder": "Your message",
                "class": "field-input",
                "rows": 5,
                "maxlength": "4000",
            }),
        }
        labels = {
            "name": "Name",
            "email": "Email",
            "phone": "Phone",
            "subject": "Subject",
            "message": "Message",
        }

    def clean_name(self):
        name = (self.cleaned_data.get("name") or "").strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter your name.")
        return name[:100]

    def clean_email(self):
        return (self.cleaned_data.get("email") or "").strip().lower()

    def clean_subject(self):
        return (self.cleaned_data.get("subject") or "").strip()[:150]

    def clean_message(self):
        message = (self.cleaned_data.get("message") or "").strip()
        if len(message) < 2:
            raise forms.ValidationError("Please enter a message.")
        if len(message) > 4000:
            raise forms.ValidationError("Message is too long.")
        return message

    def clean_website(self):
        return (self.cleaned_data.get("website") or "").strip()
