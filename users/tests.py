from mixer.backend.django import mixer
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from users.models import User


class UserSmokeTest(APITestCase):
    def test_user_empty_list(self):
        response = self.client.get(reverse('users-list'))
        self.assertIs(len(response.data), 0)

    def test_user_list(self):
        mixer.cycle(17).blend(User)
        response = self.client.get(reverse('users-list'))
        self.assertIs(len(response.data), 17)
