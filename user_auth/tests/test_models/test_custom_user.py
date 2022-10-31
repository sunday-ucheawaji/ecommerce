from django.test import TestCase
from django.utils import timezone
from user_auth.models.custom_user import CustomUser


class CustomUserTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create_user(
            email="user@gmai.com", first_name="sunday", last_name="uche", password="1298hhh")

    def setUp(self):
        self.user = CustomUser.objects.get(email="user@gmai.com")

    def test_string_representation(self):
        self.assertEquals(str(self.user), "sunday uche")

    def test_first_name_max_length(self):
        field_label = self.user._meta.get_field("first_name")
        self.assertEqual(field_label.max_length, 30)

    def test_last_name_max_length(self):
        field_label = self.user._meta.get_field("last_name")
        self.assertEqual(field_label.max_length, 30)

    def test_email_is_unique(self):
        field_label = self.user._meta.get_field("email")
        self.assertTrue(field_label.unique)

    def test_phone_max_length(self):
        field_label = self.user._meta.get_field("phone")
        self.assertEqual(field_label.max_length, 13)

    def test_is_staff_is_false(self):
        field_label = self.user._meta.get_field("is_staff")
        self.assertFalse(field_label.default)

    def test_is_superuser_is_false(self):
        field_label = self.user._meta.get_field("is_superuser")
        self.assertFalse(field_label.default)

    def test_is_active_is_true(self):
        field_label = self.user._meta.get_field("is_active")
        self.assertTrue(field_label.default)

    def test_date_joined_is_now(self):
        field_label = self.user._meta.get_field("date_joined")
        self.assertEqual(field_label.default, timezone.now)

    def test_user_type_is_customer_by_default(self):
        field_label = self.user._meta.get_field("user_type")
        self.assertEqual(field_label.default, "customer")

    def test_full_name(self):
        self.assertEqual(self.user.full_name(), "sunday uche")
