from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets

from musichub.paginators import DefaultSetPagination
from users.serializers import UserSerializer, AdminUserSerializer


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = get_user_model().objects.all()
    lookup_field = 'id'
    pagination_class = DefaultSetPagination

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminUserSerializer
        return UserSerializer
