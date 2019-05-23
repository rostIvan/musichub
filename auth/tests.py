import os
from ddt import ddt, data, unpack
from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from unittest import skipIf, TestCase
from unittest.mock import patch, MagicMock

from auth.tasks import send_email_account_activation
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
    @patch('auth.tasks.send_email_account_activation.delay')
    @data(*valid_sign_up_data)
    @unpack
    def test_successfully_sign_up(self, email, password, _mock):
        response = self.sign_up(email, password)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'email': email})
        is_login_successful = self.client.login(username=email,
                                                password=password)
        """ Because user is_active should be False """
        self.assertFalse(is_login_successful)

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
    def test_save_uuid(self):
        user_email = 'admin123@example.com'
        uuid, email = EmailVerificationUUIDStorage.save(user_email)
        self.assertIsNotNone(uuid, email)
        self.assertEqual(email, user_email)

        email = EmailVerificationUUIDStorage.get_email_by_uuid(uuid)
        self.assertEqual(email, user_email)

    def test_get_email_with_invalid_uuid(self):
        invalid_uuid = 'user-uuid-12898333-4968-4196-b823-d488455d8b91'
        with self.assertRaises(KeyError):
            EmailVerificationUUIDStorage.get_email_by_uuid(invalid_uuid)


class EmailActivationTest(APITestCase):
    @patch('auth.tasks.send_email_account_activation.delay')
    def test_send_email_account_activation(self, delay: MagicMock):
        email = 'example@email.com'
        response = self.client.post(
            reverse('sign_up'), {
                'email': email,
                'password': 'password_1234567'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        delay.assert_called_once()

    @patch('auth.verification.EmailVerificationUUIDStorage.save')
    @patch('auth.tasks.send_account_activation_message')
    def test_link_generation(self, send_mail: MagicMock, uuid: MagicMock):
        email = 'example@email.com'
        uid = '2d45d5e3-2319-448e-931e-65c48455c8ab'
        uuid.return_value = (uid, email)
        send_email_account_activation(email,
                                      lambda sub: f'http://localhost{sub}')
        send_mail.assert_called_once()

        args, _ = send_mail.call_args
        _, link = args
        self.assertTrue(uid in link)
        print(link)

    @patch('auth.verification.EmailVerificationUUIDStorage.get_email_by_uuid')
    def test_activation_user_email_exists(self, get_email):
        user = mixer.blend(User)
        self.assertFalse(user.is_active)
        get_email.return_value = user.email
        response = self.client.post(
            reverse('activate_account',
                    args=('2d45d5e3-2319-448e-931e-65c48455c8ab-',))
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(User.objects.first().is_active)

    @patch('auth.verification.EmailVerificationUUIDStorage.get_email_by_uuid')
    def test_activation_user_email_not_exists(self, get_email: MagicMock):
        user = mixer.blend(User)
        self.assertFalse(user.is_active)
        get_email.side_effect = KeyError()
        response = self.client.post(
            reverse('activate_account',
                    args=('2d45d5e3-2319-448e-931e-65c48455c8ab-',))
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.first().is_active)
