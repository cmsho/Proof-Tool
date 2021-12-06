from django.test import TestCase
from django.urls.base import reverse

from proofchecker.models import User

class StudentSignUpViewTests(TestCase):

    def test_get_context_data(self):
        """
        Verify the get_context_data method is working
        """
        response = self.client.get(reverse('student_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup_form.html')
        self.assertEqual(response.context['user_type'], 'student')

    def test_redirects_with_valid_input(self):
        response = self.client.post(reverse('student_signup'), {
            'username': 'abc',
            'email':'abc@123.com',
            'password1': '1X<ISRUkw+tuK',
            'password2': '1X<ISRUkw+tuK'
        })
        self.assertRedirects(response, reverse('login'))

class InstructorSignUpViewTestS(TestCase):

    def test_get_context_data(self):
        """
        Verify the get_context_data method is working
        """
        response = self.client.get(reverse('instructor_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup_form.html')
        self.assertEqual(response.context['user_type'], 'instructor')

    def test_redirects_with_valid_input(self):
        response = self.client.post(reverse('instructor_signup'), {
            'username': 'abc',
            'email':'abc@123.com',
            'password1': '1X<ISRUkw+tuK',
            'password2': '1X<ISRUkw+tuK'
        })
        self.assertRedirects(response, reverse('login'))

