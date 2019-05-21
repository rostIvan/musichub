from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User


class APIAuthorizeUserTestCase(APITestCase):
    def create_user(self, email, password):
        return User.objects.create_user(email, password)

    def auth(self, user, token_type, **additional_headers):
        token = AccessToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'{token_type} {token}',
                                **additional_headers)

    def jwt_auth(self, user, **additional_headers):
        self.auth(user, token_type='JWT', **additional_headers)

    def create_and_auth(self, email, password, **additional_headers):
        user = self.create_user(email, password)
        self.jwt_auth(user, **additional_headers)
        return user

    def logout(self, **additional_headers):
        self.client.credentials(**additional_headers)
