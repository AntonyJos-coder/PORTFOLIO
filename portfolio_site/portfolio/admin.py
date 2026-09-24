from django.contrib import admin
from .models import Profile, Education, Skill, Experience, Project, ContactMessage

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
        ("About sidebar", {
            "fields": ("open_to", "open_to_note", "learning_focus"),
            "description": "These fields power the “Open to” and “Currently exploring” cards next to About.",
        }),
        ("Resume", {"fields": ("resume_file",)}),
        ("Contact details", {"fields": ("phone", "email", "location")}),
        ("Social links", {"fields": ("instagram_url", "facebook_url", "linkedin_url", "github_url")}),
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
    list_display = ("title", "summary", "featured", "order", "created_at")
    list_editable = ("featured", "order")
    list_filter = ("featured",)
    search_fields = ("title", "summary", "tech_stack")


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
