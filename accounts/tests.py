from django.test import TestCase
from django.contrib.auth import get_user_model

class UsersTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='password',
            name='Test User',
            username='testuser',
            first_name='Test',
            about='This is a test user',
            nickname='Tester',
            car=True,
            car_num='1234가5678',
            major='Computer Science',
        )
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@test.com',
            password='password',
            name='Admin User',
            username='adminuser',
            first_name='Admin',
            about='This is an admin user',
            nickname='Admin',
            car=True,
            car_num='1234나5678',
            major='Information Science',
        )

    def test_create_user(self):
        user = self.user
        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(user.name, 'Test User')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.about, 'This is a test user')
        self.assertEqual(user.nickname, 'Tester')
        self.assertEqual(user.car, True)
        self.assertEqual(user.car_num, '1234가5678')
        self.assertEqual(user.major, 'Computer Science')
        self.assertEqual(user.is_active, True)
        # self.assertEqual(user.is_staff, False)
        self.assertEqual(user.premium, False)

    def test_create_superuser(self):
        admin_user = self.admin_user
        self.assertEqual(admin_user.email, 'admin@test.com')
        self.assertEqual(admin_user.name, 'Admin User')
        self.assertEqual(admin_user.username, 'adminuser')
        self.assertEqual(admin_user.first_name, 'Admin')
        self.assertEqual(admin_user.about, 'This is an admin user')
        self.assertEqual(admin_user.nickname, 'Admin')
        self.assertEqual(admin_user.car, True)
        self.assertEqual(admin_user.car_num, '1234나5678')
        self.assertEqual(admin_user.major, 'Information Science')
        self.assertEqual(admin_user.is_active, True)
        self.assertEqual(admin_user.is_staff, True)
        self.assertEqual(admin_user.premium, False)