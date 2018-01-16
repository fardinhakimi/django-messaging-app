from django.test import TestCase
from django.contrib.auth.models import User
from .forms import AuthenticationForm, RegistrationForm



class TestRegistrationForm(TestCase):


    def setUp(self):

        self.user = User.objects.create(username = "fardin", first_name= "fardin", password = "test1234")

    def test_username_field_label(self):

        form = RegistrationForm()

        self.assertTrue(form.fields['username'].label == 'Username')

    def test_UserForm_valid(self):

        form = RegistrationForm(data={'username': "zohra",
                                      'password': "testing1234",
                                      'first_name': "zohra"
                                      })

        self.assertTrue(form.is_valid())

    def test_form_is_invalid_duplicate_username(self):

        form_data = {'username': "fardin",
                     "first_name": "fardin",
                     "password": "test1234"
                     }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_required_data(self):
        form = RegistrationForm(
            data={'username': "",
                  'password': "testing1234",
                  'first_name': ""
                  }
        )
        self.assertFalse(form.is_valid())

        self.assertEqual(form.errors, {
            'first_name': ['This field is required.'],
            'username': ['This field is required.'],
        })




class TestAuthenticationForm(TestCase):

    def setUp(self):

        self.user = User.objects.create(username = "fardin", password = "test1234")

    def test_failed_authentication(self):
        form_data = {'username': "unknown", "password" :"incorrect" }
        form = AuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())


    def test_username_field_label(self):

        form = AuthenticationForm()

        self.assertTrue(form.fields['username'].label == 'Username')



