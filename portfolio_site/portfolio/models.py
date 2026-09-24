from django.db import models
from django.core.validators import FileExtensionValidator, RegexValidator

IMAGE_EXTENSIONS = FileExtensionValidator(["jpg", "jpeg", "png", "webp"])
PDF_EXTENSIONS = FileExtensionValidator(["pdf"])


def csv_list(value):
    return [item.strip() for item in (value or "").split(",") if item.strip()]


class Profile(models.Model):
    """Singleton-style model holding the site owner's core info."""
    full_name = models.CharField(max_length=100, default="Antony Jos")
    title = models.CharField(max_length=100, default="Computer Engineer",
                              help_text="e.g. Computer Engineer")
    tagline = models.CharField(max_length=150, default="Hi, I'm Antony Jos.",
                                help_text="Big hero heading, e.g. \"Hi, I'm Antony Jos.\"")
    subtitle = models.CharField(max_length=200, blank=True,
                                 help_text="Small line under the hero heading")
    about = models.TextField(help_text="The About Me / Profile summary paragraph(s)")
    learning_focus = models.CharField(
        max_length=200, blank=True,
        help_text="Currently exploring chips. Comma-separated, e.g. Data Analytics, Web Development"
    )
    open_to = models.CharField(
        max_length=120, blank=True,
        default="Internships & junior roles",
        help_text="Main line in the About sidebar “Open to” card"
    )
    open_to_note = models.CharField(
        max_length=200, blank=True,
        default="Web, applications, and data analytics work",
        help_text="Supporting line under “Open to”"
    )
    profile_image = models.ImageField(
        upload_to="profile/", blank=True, null=True,
        validators=[IMAGE_EXTENSIONS],
        help_text="Your photo for the hero section. A square image (about 600×600) works best. JPG, PNG or WebP only."
    )
    resume_file = models.FileField(
        upload_to="resume/", blank=True, null=True,
        validators=[PDF_EXTENSIONS],
        help_text="Upload a PDF resume for the Resume button"
    )
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    footer_note = models.CharField(max_length=150, blank=True,
                                    default="Built with Django")

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"

    def __str__(self):
        return self.full_name

    @property
    def learning_focus_list(self):
        return csv_list(self.learning_focus)

    def save(self, *args, **kwargs):
        # keep this a singleton: always pk=1
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass


class Education(models.Model):
    school = models.CharField(max_length=150)
    degree = models.CharField(max_length=150, help_text="e.g. Diploma in Computer Engineering")
    start_year = models.CharField(max_length=10, blank=True,
                                   help_text="Leave blank if you only want to show a completion year")
    end_year = models.CharField(max_length=10, blank=True, help_text="Leave blank if ongoing")
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first")

    class Meta:
        ordering = ["order", "-start_year"]
        verbose_name_plural = "Education"

    def __str__(self):
        return f"{self.degree} — {self.school}"

    @property
    def years_label(self):
        if self.start_year and self.end_year:
            return f"{self.start_year} – {self.end_year}"
        if self.start_year and not self.end_year:
            return f"{self.start_year} – Present"
        if self.end_year:
            return f"Completed {self.end_year}"
        return ""


class Skill(models.Model):
    LEVEL_CHOICES = [
        (1, "Beginner"),
        (2, "Intermediate"),
        (3, "Advanced"),
        (4, "Expert"),
    ]
    CATEGORY_CHOICES = [
        ("programming", "Programming"),
        ("web", "Web"),
        ("backend", "Backend"),
        ("database", "Database"),
        ("app", "Application Development"),
        ("other", "Other"),
    ]
    name = models.CharField(max_length=60)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="programming")
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, default=3)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Experience(models.Model):
    TYPE_CHOICES = [
        ("internship", "Internship / Industrial Training"),
        ("training", "Training"),
        ("work", "Work Experience"),
    ]
    organization = models.CharField(max_length=150)
    role = models.CharField(max_length=150, blank=True,
                             help_text="Leave blank to fall back to the experience type label")
    exp_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="internship")
    location = models.CharField(max_length=120, blank=True)
    start_date = models.CharField(max_length=30, help_text="e.g. 15 May 2023")
    end_date = models.CharField(max_length=30, blank=True,
                                 help_text="Leave blank for a single-day entry or if ongoing")
    description = models.TextField(blank=True,
                                    help_text="What you did / learned — easy to fill in or edit later")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-start_date"]
        verbose_name_plural = "Experience"

    def __str__(self):
        return f"{self.role or self.get_exp_type_display()} — {self.organization}"

    @property
    def display_role(self):
        return self.role or self.get_exp_type_display()

    @property
    def date_label(self):
        if self.end_date and self.end_date != self.start_date:
            return f"{self.start_date} – {self.end_date}"
        return self.start_date


class Project(models.Model):
    title = models.CharField(max_length=120)
    summary = models.CharField(max_length=250, help_text="Short one-line summary")
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="projects/", blank=True, null=True,
        validators=[IMAGE_EXTENSIONS],
    )
    project_url = models.URLField(blank=True, help_text="Live site / demo link")
    source_url = models.URLField(blank=True, help_text="Code repository link")
    tech_stack = models.CharField(max_length=200, blank=True,
                                   help_text="Comma-separated, e.g. Django, HTML, CSS")
    featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

    @property
    def tech_list(self):
        return csv_list(self.tech_stack)


class ContactMessage(models.Model):
    phone_validator = RegexValidator(
        regex=r"^[\d\+\-\s\(\)]{7,20}$",
        message="Enter a valid phone number."
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, validators=[phone_validator])
    subject = models.CharField(max_length=150, blank=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.name} ({self.submitted_at:%Y-%m-%d})"
