from django.test import TestCase
from apps.core.models import CustomUser, Address


class CustomUserTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email='abolfazlrasouli@gmail.com',
            phone_number='09121234567',
            birthday='2000-01-01',
            role=CustomUser.CUSTOMERUSER_CUSTOMER,
            is_deleted=False,
            username='abolfazl',
            password='123456zx!'
        )
        self.address = Address.objects.create(
            user=self.user,
            country='Iran',
            province='Tehran',
            city='Tehran',
            street='Main Street',
            pelak='1234',
            complete_address='Main Street, Tehran, Iran'
        )

    def test_delete_method_sets_is_deleted_to_true(self):
        self.user.delete()
        self.assertTrue(self.user.is_deleted)

    def test_undelete_method_sets_is_deleted_to_false(self):
        self.user.is_deleted = True
        self.user.save()
        self.user.undelete()
        self.assertFalse(self.user.is_deleted)

    def test_deleted_manager_only_returns_deleted_objects(self):
        self.user.is_deleted = True
        self.user.save()
        deleted_users = CustomUser.objects.deleted()
        self.assertIn(self.user, deleted_users)

    def test_archive_manager_returns_all_objects(self):
        all_users = CustomUser.objects.archive()
        self.assertIn(self.user, all_users)

    def test_get_queryset_only_returns_non_deleted_objects(self):
        non_deleted_users = CustomUser.objects.get_queryset()
        self.assertIn(self.user, non_deleted_users)
        self.user.is_deleted = True
        self.user.save()
        self.assertIn(self.user, non_deleted_users)

    def test_str_method(self):
        test_str = f'{self.user.username} - {self.address.city} - {self.address.street}'
        self.assertEqual(str(self.address), test_str)
