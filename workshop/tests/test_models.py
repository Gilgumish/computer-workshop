from django.test import TestCase
from workshop.models import User, Component


class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password12345"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("password12345"))


class ComponentModelTest(TestCase):
    def test_component_creation(self):
        component = Component.objects.create(
            name="Test Component",
            specifications="Some specifications",
            price=100.00,
            type="CPU",
        )
        self.assertEqual(component.name, "Test Component")
        self.assertEqual(component.specifications, "Some specifications")
        self.assertEqual(component.price, 100.00)
        self.assertEqual(component.type, "CPU")
