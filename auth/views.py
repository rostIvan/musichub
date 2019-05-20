from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import AllowAny

from auth.serializers import SignUpSerializer


class SignUpView(generics.CreateAPIView):
    model = get_user_model()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)
