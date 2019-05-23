from django.contrib.auth import get_user_model
from rest_framework import generics, views, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from auth.serializers import SignUpSerializer
from auth.verification import EmailVerificationUUIDStorage
from users.models import User


class SignUpView(generics.CreateAPIView):
    model = get_user_model()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)


class AccountActivationView(views.APIView):
    def get(self, request, uuid):
        try:
            email = EmailVerificationUUIDStorage.get_email_by_uuid(uuid)
            try:
                self.activate_user(email)
                return Response({'account': 'activated'},
                                status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def activate_user(self, email):
        user = User.objects.get(email=email)
        user.is_active = True
        user.save(update_fields=['is_active'])
