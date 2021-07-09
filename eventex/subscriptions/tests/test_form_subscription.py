from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionFormTest(TestCase):

    def test_form_has_fields(self):
        """Form must have for fields"""
        form = SubscriptionForm()
        expected = ['name', 'cpf', 'email', 'phone']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_cpf_is_digit(self):
        """Cpf must only accepty digits"""
        form = self.make_validated_form(cpf='ABCD5678901')
        self.assertFormCode(form, 'cpf', 'digits')

    def test_cpf_11_digits(self):
        """Cpf must have 11 digits"""
        form = self.make_validated_form(cpf='1234')
        self.assertFormCode(form, 'cpf', 'length')

    def test_name_must_be_capitalized(self):
        """Name must be capitalized"""
        # TALVANE augusto -> Talvane Augusto
        form = self.make_validated_form(name='TALVANE augusto de magalhães')
        self.assertEqual(
            'Talvane Augusto De Magalhães',
            form.cleaned_data['name']
        )

    def test_email_is_optional(self):
        """Email is optional"""
        form = self.make_validated_form(email='')
        self.assertFalse(form.errors)

    def test_phone_is_optional(self):
        """Phone is optional"""
        form = self.make_validated_form(phone='')
        self.assertFalse(form.errors)

    def test_must_inform_email_or_phone(self):
        """Email and Phone are optional, but one must be informed"""
        form = self.make_validated_form(phone='', email='')
        self.assertListEqual(['__all__'], list(form.errors))

    def assertFormCode(self, form, field, code):
        errors = form.errors.as_data()
        errors_list = errors[field]
        exceptions = errors_list[0]

        self.assertEqual(code, exceptions.code)

    def assertFormErrorMessage(self, form, field, msg):
        errors = form.errors
        errors_list = errors[field]
        self.assertListEqual([msg], errors_list)

    def make_validated_form(self, **kwargs):
        valid = dict(name="Talvane Augusto", cpf="12345678901",
                     email="talvane.magalhaes@gmail.com", phone="99999999999")
        data = dict(valid, **kwargs)
        form = SubscriptionForm(data)
        form.is_valid()

        return form
