from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Talvane Augusto de Magalhães',
                    cpf='12345678901',
                    email='talvane.magalhaes@gmail.com',
                    phone='81-99999-9999')
        self.client.post(r('subscriptions:new'), data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        """Valid send subscription email subject"""
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        """Valid send subscription email from"""
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        """Valid send subscription email to"""
        expect = ['contato@eventex.com.br', 'talvane.magalhaes@gmail.com']
        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        """Valid send subscription email body"""
        contents = [
            'Talvane Augusto de Magalhães',
            '12345678901',
            'talvane.magalhaes@gmail.com',
            '81-99999-9999',
        ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
