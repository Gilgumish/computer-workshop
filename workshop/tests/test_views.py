from django.test import TestCase
from django.urls import reverse
from workshop.models import User


class HomeViewTest(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse("workshop:home"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("num_computers", response.context)
        self.assertIn("num_components", response.context)
        self.assertIn("num_masters", response.context)


class LoginViewTest(TestCase):
    def test_login_view_get(self):
        url = reverse("workshop:login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")


class RegisterViewTest(TestCase):
    def test_register_view_get(self):
        url = reverse("workshop:register")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register")

    def test_register_view_post(self):
        url = reverse("workshop:register")
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
        }
        response = self.client.post(url, form_data)
        if response.status_code == 200:
            print(response.context["form"].errors)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="testuser").exists())


class AvailableComputersViewTest(TestCase):
    def test_available_computers_view(self):
        url = reverse("workshop:available_computers")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("computers", response.context)
