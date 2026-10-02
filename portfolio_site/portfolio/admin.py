from django.contrib import admin

try:
    from .models import (
        Profile,
        Education,
        Skill,
        Experience,
        Project,
        ContactMessage,
    )
except ImportError:
    from portfolio.models import (
        Profile,
        Education,
        Skill,
        Experience,
        Project,
        ContactMessage,
    )

admin.site.site_header = "Antony Jos Portfolio"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Manage site content"


class FastAdmin(admin.ModelAdmin):
    list_per_page = 50
    show_full_result_count = False
    save_on_top = True


@admin.register(Profile)
class ProfileAdmin(FastAdmin):
    fieldsets = (
        ("Identity", {"fields": ("full_name", "title", "tagline", "subtitle", "about", "profile_image")}),
        ("About focus & highlights", {
            "fields": ("about_focus", "about_approach", "about_currently", "location", "open_to", "open_to_note", "learning_focus"),
            "description": "These fields control the Focus, Approach, Currently, and Based in items in the About section.",
        }),
        ("Resume", {"fields": ("resume_file",)}),
        ("Contact details", {"fields": ("phone", "email")}),
        ("Social links", {"fields": ("github_url", "linkedin_url", "facebook_url")}),
        ("Footer", {"fields": ("footer_note",)}),
    )

    def has_add_permission(self, request):
        return not Profile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Education)
class EducationAdmin(FastAdmin):
    list_display = ("degree", "school", "start_year", "end_year", "order")
    list_editable = ("order",)
    ordering = ("order",)


@admin.register(Skill)
class SkillAdmin(FastAdmin):
    list_display = ("name", "category", "level", "order")
    list_editable = ("category", "level", "order",)
    list_filter = ("category",)
    ordering = ("category", "order")
    search_fields = ("name",)


@admin.register(Experience)
class ExperienceAdmin(FastAdmin):
    list_display = ("organization", "display_role", "exp_type", "start_date", "end_date", "order")
    list_editable = ("order",)
    list_filter = ("exp_type",)
    ordering = ("order",)
    search_fields = ("organization", "role")


@admin.register(Project)
class ProjectAdmin(FastAdmin):
    list_display = ("title", "category", "date_range", "has_live_demo", "order")
    list_editable = ("order",)
    list_filter = ("category", "featured")
    search_fields = ("title", "category", "summary", "tech_stack")
    fieldsets = (
        ("Project Details", {
            "fields": ("title", "category", "date_range", "summary", "description", "image")
        }),
        ("Live Demo & Code Links", {
            "fields": ("project_url", "source_url"),
            "description": "Live Demo: Enter a URL to automatically show the 'Live Demo ↗' button on the project card. Leave blank to hide it. Code Repository: Links to the 'View Code ↗' button.",
        }),
        ("Technologies & Display", {
            "fields": ("tech_stack", "featured", "order")
        }),
    )

    @admin.display(boolean=True, description="Live Demo Active")
    def has_live_demo(self, obj):
        return bool(obj.project_url)


@admin.register(ContactMessage)
class ContactMessageAdmin(FastAdmin):
    list_display = ("name", "email", "subject", "submitted_at", "is_read")
    list_filter = ("is_read", "submitted_at")
    list_editable = ("is_read",)
    search_fields = ("name", "email", "message")
    readonly_fields = ("name", "email", "phone", "subject", "message", "submitted_at")
    date_hierarchy = "submitted_at"

    def has_add_permission(self, request):
        return False
