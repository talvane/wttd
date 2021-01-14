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
