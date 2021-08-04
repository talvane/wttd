from django.core.exceptions import ValidationError
from django.test import TestCase
from eventex.core.models import Speaker, Contact


class ContactModelTest(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(
            name='Talvane Augusto',
            slug='talvane-augusto',
            photo='http://hbn.link/hb-pic'
        )

    def test_email(self):
        Contact.objects.create(
            speaker=self.speaker,
            kind=Contact.EMAIL,
            value='talvane.magalhaes@gmail.com'
        )

        self.assertTrue(Contact.objects.exists())

    def test_phone(self):
        Contact.objects.create(
            speaker=self.speaker,
            kind=Contact.PHONE,
            value='81999428928'
        )

        self.assertTrue(Contact.objects.exists())

    def test_choices(self):
        """Contact kind should be limited to E or P"""
        contact = Contact(speaker=self.speaker, kind='A', value='B')
        self.assertRaises(ValidationError, contact.full_clean)

    def test_str(self):
        contact = Contact(
            speaker=self.speaker,
            kind=Contact.EMAIL,
            value='talvane.magalhaes@gmail.com'
        )
        self.assertEqual('talvane.magalhaes@gmail.com', str(contact))
