from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from workshop.admin import UserAdmin
from workshop.models import User


class MockRequest:
    pass


class UserAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.user_admin = UserAdmin(User, self.site)
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password12345"
        )

    def test_user_admin_get_queryset(self):
        request = MockRequest()
        queryset = self.user_admin.get_queryset(request)
        self.assertIn(self.user, queryset)

    def test_user_admin_display(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.username, "testuser")
