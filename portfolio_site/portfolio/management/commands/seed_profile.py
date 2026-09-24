from django.core.management.base import BaseCommand
from portfolio.models import Profile, Education, Skill, Experience, Project


class Command(BaseCommand):
    help = "Seed the database with Antony Jos's verified portfolio content."

    def handle(self, *args, **options):
        profile, _ = Profile.objects.get_or_create(pk=1)
        profile.full_name = "Antony Jos"
        profile.title = "Computer Engineer"
        profile.tagline = "Hi, I'm Antony Jos."
        profile.subtitle = "Computer Engineer building practical web, application and data-driven solutions."
        profile.about = (
            "I hold a Diploma in Computer Engineering from Carmel Polytechnic College, "
            "Alappuzha (2025). I build practical projects across web development, "
            "application development and data analytics, working hands-on with Python, "
            "Java, C, SQL, Spring Boot, MongoDB and Flutter. I enjoy turning ideas into "
            "working software and I'm continuing to sharpen my skills, with a particular "
            "interest in data analytics."
        )
        # Real contact details, resume and social links are intentionally left blank —
        # add them from /admin (Profile). Nothing fake is shown on the public site
        # until they're filled in.
        profile.learning_focus = "Data Analytics, Web Development, Application Development"
        profile.open_to = "Internships & junior roles"
        profile.open_to_note = "Web, applications, and data analytics work"
        profile.phone = ""
        profile.email = ""
        profile.location = ""
        profile.footer_note = "Built with Django, HTML, CSS and JavaScript."
        profile.save()

        Education.objects.all().delete()
        Education.objects.create(
            school="Carmel Polytechnic College, Alappuzha",
            degree="Diploma in Computer Engineering",
            start_year="",
            end_year="2025",
            description="",
            order=1,
        )

        Skill.objects.all().delete()
        skills = [
            ("C", "programming", 1),
            ("Python", "programming", 2),
            ("Java", "programming", 3),
            ("HTML", "web", 4),
            ("Spring Boot", "backend", 5),
            ("SQL", "database", 6),
            ("MongoDB", "database", 7),
            ("Flutter", "app", 8),
        ]
        for name, category, order in skills:
            Skill.objects.create(name=name, category=category, level=3, order=order)

        Experience.objects.all().delete()
        Experience.objects.create(
            organization="BSNL Regional Telecom Training Centre, Alappuzha",
            role="",
            exp_type="training",
            start_date="15 May 2023",
            end_date="",
            description="",
            order=1,
        )
        Experience.objects.create(
            organization="Verdant, Ernakulam",
            role="",
            exp_type="internship",
            start_date="6 June 2024",
            end_date="",
            description="",
            order=2,
        )

        Project.objects.all().delete()
        Project.objects.create(
            title="Personal Portfolio Website",
            summary="A Django-powered portfolio with an admin-managed backend for easy content updates.",
            description=(
                "Built with Django, HTML, CSS and JavaScript. Profile details, skills, "
                "education, experience and projects are all editable from the Django "
                "admin panel without touching any code — this website is itself the project."
            ),
            tech_stack="Django, Python, HTML, CSS, JavaScript",
            featured=True,
            order=1,
        )

        self.stdout.write(self.style.SUCCESS(
            "Verified profile content seeded. Visit /admin to add a resume PDF, "
            "email, GitHub/LinkedIn links and more projects."
        ))
