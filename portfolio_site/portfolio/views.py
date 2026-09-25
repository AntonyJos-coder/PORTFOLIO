from collections import OrderedDict

from django.conf import settings
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from .forms import ContactForm
from .models import Profile, Education, Skill, Experience, Project
from .page_cache import HOME_CACHE_KEY

CONTACT_RATE_LIMIT = 5
CONTACT_RATE_WINDOW = 60 * 60
PAGE_CACHE_TTL = 120


def _client_ip(request):
    return request.META.get("REMOTE_ADDR") or "unknown"


def _contact_over_limit(request):
    return cache.get(f"contact-rate:{_client_ip(request)}", 0) >= CONTACT_RATE_LIMIT


def _bump_contact_rate(request):
    key = f"contact-rate:{_client_ip(request)}"
    cache.set(key, cache.get(key, 0) + 1, CONTACT_RATE_WINDOW)


def _group_skills(skills):
    groups = OrderedDict()
    for skill in skills:
        group = groups.setdefault(skill.category, {
            "key": skill.category,
            "label": skill.get_category_display(),
            "skills": [],
        })
        group["skills"].append(skill)
    return list(groups.values())


def _send_contact_notification(form_data):
    """Email the site owner when a contact message arrives."""
    notify_email = getattr(settings, "CONTACT_NOTIFY_EMAIL", "")
    if not notify_email:
        return
    subject = (
        f"[Portfolio] New message from {form_data['name']}"
        + (f" — {form_data['subject']}" if form_data.get("subject") else "")
    )
    body = (
        f"Name:    {form_data['name']}\n"
        f"Email:   {form_data['email']}\n"
        f"Phone:   {form_data.get('phone') or '—'}\n"
        f"Subject: {form_data.get('subject') or '—'}\n"
        f"\n{form_data['message']}\n"
        f"\n---\nReply directly to this email to respond."
    )
    try:
        EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[notify_email],
            reply_to=[form_data["email"]],
        ).send(fail_silently=True)
    except Exception:
        pass  # never crash the page over a failed email


def _page_payload():
    cached = cache.get(HOME_CACHE_KEY)
    if cached is not None:
        return cached

    try:
        profile = Profile.objects.get(pk=1)
    except Profile.DoesNotExist:
        profile = Profile(full_name="Antony Jos", title="Computer Engineer")

    education = list(Education.objects.all())
    skills = list(Skill.objects.all())
    experience = list(Experience.objects.all())
    projects = list(Project.objects.all())
    featured_project = next((project for project in projects if project.featured), None)
    other_projects = [
        project for project in projects
        if featured_project is None or project.pk != featured_project.pk
    ]

    payload = {
        "profile": profile,
        "education": education,
        "grouped_skills": _group_skills(skills),
        "experience": experience,
        "featured_project": featured_project,
        "other_projects": other_projects,
    }
    cache.set(HOME_CACHE_KEY, payload, PAGE_CACHE_TTL)
    return payload


@csrf_protect
@never_cache
def home(request):
    if request.method == "POST":
        if _contact_over_limit(request):
            messages.error(request, "Please wait a bit before sending another message.")
            form = ContactForm()
        else:
            form = ContactForm(request.POST)
            if form.is_valid():
                if not form.cleaned_data.get("website"):
                    form.save()
                    _send_contact_notification(form.cleaned_data)
                    _bump_contact_rate(request)
                messages.success(request, "Thanks for reaching out! I'll get back to you soon.")
                return redirect(reverse("home") + "#contact")
            messages.error(request, "Please fix the errors below and try again.")
    else:
        form = ContactForm()

    context = dict(_page_payload())
    context["form"] = form
    return render(request, "portfolio/home.html", context)
