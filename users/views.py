from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets

from users.serializers import UserSerializer, AdminUserSerializer


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = get_user_model().objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminUserSerializer
        return UserSerializer
