from django.test import TestCase
from django.urls import reverse

from portfolio.models import Profile


class HomeViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Profile.objects.create(
            pk=1,
            full_name="Antony Jos",
            title="Computer Engineer",
            about="Test about copy.",
            open_to="Internships & junior roles",
            open_to_note="Web, applications, and data analytics work",
            learning_focus="Data Analytics, Web Development",
        )

    def test_home_ok(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Open to")
        self.assertContains(response, "Currently exploring")
        self.assertContains(response, "Internships")

    def test_contact_rejects_short_message(self):
        response = self.client.post(reverse("home"), {
            "name": "Alex",
            "email": "alex@example.com",
            "message": "Hi",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "slightly longer message")

    def test_contact_honeypot_does_not_store(self):
        from portfolio.models import ContactMessage
        self.client.post(reverse("home"), {
            "name": "Bot",
            "email": "bot@example.com",
            "message": "This is a long enough spam message.",
            "website": "https://spam.example",
        })
        self.assertEqual(ContactMessage.objects.count(), 0)
