from datetime import date
from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm, FUTURE_DOB_ERROR, PAST_DOB_ERROR

User = get_user_model()


class CreationFormTest(TestCase):

    def test_valid_user_form(self):
        form = CustomUserCreationForm(
            data={
                'username': 'juan',
                'email': 'test@email.com',
                'password1': 'testpass123',
                'password2': 'testpass123',
                'day': '01',
                'month': '12',
                'year': '1995'
            }
        )
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_cannot_have_future_dob(self):
        form = CustomUserCreationForm(
            data={
                'username': 'juan',
                'email': 'test@email.com',
                'password1': 'testpass123',
                'password2': 'testpass23',
                'day': '01',
                'month': '12',
                'year': '2100'
            }
        )
        form.full_clean()
        self.assertEqual(form.errors['year'], [FUTURE_DOB_ERROR])

    def test_dob_more_than_90_years_ago_is_not_valid(self):
        form = CustomUserCreationForm(
            data={
                'username': 'juan',
                'email': 'test@email.com',
                'password1': 'testpass123',
                'password2': 'testpass23',
                'day': '01',
                'month': '12',
                'year': '1905'
            }
        )
        form.full_clean()
        self.assertEqual(form.errors['year'], [PAST_DOB_ERROR])

    def test_successful_form_creates_new_user(self):
        form = CustomUserCreationForm(
            data={
                'username': 'juan',
                'email': 'test@email.com',
                'password1': 'testpass123',
                'password2': 'testpass123',
                'day': '01',
                'month': '12',
                'year': '1995'
            }
        )
        form.save()
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(User.objects.first().dob, date(1995, 12, 1))
