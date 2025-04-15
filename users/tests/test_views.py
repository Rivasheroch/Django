from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm

User = get_user_model()

class UserViewTests(TestCase):

    def test_home_view_get(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/home.html')

    def test_signup_valid(self):
        response = self.client.post(reverse('home'), {
            'signup': True,
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'password123',
            'password2': 'password123',
            'user_type': 'normal_user',
        })
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertEqual(len(messages.get_messages(response.wsgi_request)), 1)  # Check for success message

    def test_signup_invalid_email(self):
        response = self.client.post(reverse('home'), {
            'signup': True,
            'username': 'testuser',
            'email': 'invalid-email',
            'password1': 'password123',
            'password2': 'password123',
            'user_type': 'normal_user',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='testuser').exists())
        self.assertIn('Enter a valid email address', str(response.content))

    def test_login_view(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            is_active=False  # User should not be active
        )
        response = self.client.post(reverse('home'), {
            'login': True,
            'username': 'testuser',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Your account is not active', str(response.content))

    def test_activate_view(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            is_active=False
        )
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        response = self.client.get(reverse('activate', args=[uid, token]))
        self.assertRedirects(response, reverse('dashboard'))
        user.refresh_from_db()
        self.assertTrue(user.is_active)

    def test_logout_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'))
        self.assertNotIn('_auth_user_id', self.client.session)  # Check that the user is logged out
