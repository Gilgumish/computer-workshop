from django.test import TestCase
from workshop.forms import CustomUserCreationForm


class CustomUserCreationFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
        }
        form = CustomUserCreationForm(data=form_data)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": "StrongPassword123!",
            "password2": "DifferentPassword123!",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
