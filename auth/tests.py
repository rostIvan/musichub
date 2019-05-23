import os
from ddt import ddt, data, unpack
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from unittest import skipIf, TestCase

from auth.verification import EmailVerificationUUIDStorage
from users.models import User

valid_sign_up_data = (
    # (email, password)
    ('admin@gmail.com', 'admin_qwerty'),
    ('admin@example.com', 'admin_qwerty'),
    ('django@example.com', '1234_django_example'),
    ('vasya@nelox.com', 'vasya_chotkiy'),
)

invalid_sign_up_data = (
    # (email, password, expected_response)
    ('', '', {
        'email': ['This field may not be blank.'],
        'password': ['This field may not be blank.']
    }),

    ('@wrong_email.com', 'some_password', {
        'email': ['Enter a valid email address.']
    }),

    ('valid_email1@example.com', '_123', {
        'password': ['This password is too short. '
                     'It must contain at least 8 characters.']
    }),
    ('valid_email2@example.com', 'qwerty', {
        "password": [
            "This password is too short. "
            "It must contain at least 8 characters.",
            "This password is too common."
        ]
    }),
)


@ddt
class APIUserSignUpTest(APITestCase):
    @data(*valid_sign_up_data)
    @unpack
    def test_successfully_sign_up(self, email, password):
        response = self.sign_up(email, password)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'email': email})
        is_login_successful = self.client.login(username=email,
                                                password=password)
        self.assertTrue(is_login_successful)

        self.assertIs(User.objects.count(), 1)
        user = User.objects.first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, email)
        self.assertIsNotNone(user.password)
        self.assertTrue(user.password.startswith('argon2'))

    @data(*invalid_sign_up_data)
    @unpack
    def test_unsuccessfully_sign_up(self, email, password, expected_response):
        response = self.sign_up(email, password)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response)
        self.assertFalse(User.objects.exists())

    def sign_up(self, email, password):
        return self.client.post(
            reverse('sign_up'),
            {'email': email, 'password': password}
        )


@skipIf(os.getenv('RUN_REDIS_TESTS') != 'yep', "Redis run only locally")
class RedisEmailUUIDStorageTest(TestCase):
    def test_some(self):
        uuid, email = EmailVerificationUUIDStorage.save('admin123@example.com')
        print(uuid, email)
        email = EmailVerificationUUIDStorage.get_email_by_uuid(uuid)
        print(email)
