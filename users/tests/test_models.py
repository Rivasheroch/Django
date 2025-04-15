from django.test import TestCase
from .models import CustomUser

class CustomUserModelTests(TestCase):

    def test_user_creation(self):
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            user_type='normal_user'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertFalse(user.is_active)  # User should not be active by default
