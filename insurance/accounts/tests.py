from django.test import TestCase
from django.contrib.auth.models import User
from django.core import mail

from .forms import UserRegisterForm
import re

class UserRegisterFormTest(TestCase):
    def test_login_email_are_same(self):
        form = UserRegisterForm(data = {
            'email': 'alice@example.net',
            'password1': '@xi2*(2-139|',
            'password2': '@xi2*(2-139|'
        })
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertEqual(user.username, user.email)

    def test_passwords_dont_match(self):
        form = UserRegisterForm(data = {
            'email': 'alice@example.net',
            'password1': '1@xi2*(2-139|',
            'password2': '@xi2*(2-139|'
        })
        self.assertFalse(form.is_valid())

class UserRegisterViewTest(TestCase):
    def test_redirect_to_login_page(self):
        data = {
            'email': 'alice@example.net',
            'password1': '@xi2*(2-139|',
            'password2': '@xi2*(2-139|'
        }
        response = self.client.post('/accounts/register/', data)
        self.assertRedirects(response, '/accounts/login/')


class UserResetPwTest(TestCase):
    def test_reset_pw_email(self):
        email = 'alice@example.net'
        user = User.objects.create_user(email, email, '@xi2*(2-139|')
        user.save()
        response = self.client.post('/accounts/reset_password/', {'email': email})
        
        self.assertEqual(len(mail.outbox), 1)
        url = re.search(r'(https?://\S+?/reset/\S+)', mail.outbox[0].body).group(1)
        response1 = self.client.get(url, follow=True)
        self.assertTemplateUsed(response1, 'password_reset_confirm.html')

        

