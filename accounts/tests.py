from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from accounts import views

def login_test_user(self):
        self.adminuser = User.objects.create_user('admin', 'admin@test.com', 'pass')
        self.adminuser.save()
        self.client.login(username='admin', password='pass')
        
class LoginTests(TestCase):
    
    def setUp(self):
        self.adminuser = User.objects.create_user('admin', 'admin@test.com', 'pass')
        self.adminuser.save()
        
    def test_user_with_correct_credentials_log_in(self):
        response = self.client.post(reverse("accounts:login"), {"username":"admin", "password":"pass"})
        self.assertRedirects(response, reverse("backend:index"))

    def test_user_with_wrong_username_log_in(self):
        response = self.client.post(reverse("accounts:login"), {"username":"wrong", "password":"pass"})
        self.assertContains(response, views.WRONG_CREDENTIALS)

    def test_user_with_wrong_password_log_in(self):
        response = self.client.post(reverse("accounts:login"), {"username":"admin", "password":"wrong"})
        self.assertContains(response, views.WRONG_CREDENTIALS)
        
    def test_user_with_empty_username_log_in(self):
        response = self.client.post(reverse("accounts:login"), {"password":"pass"})
        self.assertContains(response, views.WRONG_CREDENTIALS)

    def test_user_with_empty_password_log_in(self):
        response = self.client.post(reverse("accounts:login"), {"username":"admin"})
        self.assertContains(response, views.WRONG_CREDENTIALS)

    def test_user_with_inactive_account(self):
        self.adminuser = User.objects.create_user('inactive', 'admin@test.com', 'pass')
        self.adminuser.is_active = False
        self.adminuser.save()
        response = self.client.post(reverse("accounts:login"), {"username":"inactive", "password":"pass"})
        self.assertContains(response, views.INACTIVE_ACCOUNT)
        
    def test_user_with_not_existing_account(self):
        response = self.client.post(reverse("accounts:login"), {"username":"account", "password":"pass123"})
        self.assertContains(response, views.WRONG_CREDENTIALS )
        
class LogoutTests(TestCase):
    
    def setUp(self):
        login_test_user(self)
        
    def test_can_enter_backend(self):
        response = self.client.get(reverse("backend:index"))
        self.assertEqual(response.status_code, 200)
        
    def test_can_logout(self):
        response = self.client.get(reverse("accounts:logout"))
        self.assertRedirects(response, reverse("articles:index"))
        response = self.client.get(reverse("backend:index"))
        self.assertRedirects(response, '%s?next=/backend/' % reverse("accounts:login"))
        
