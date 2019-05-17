from django.urls import path

from users.views import UserViewSet

urlpatterns = [
    path('', UserViewSet.as_view({'get': 'list'})),
    path('<int:id>', UserViewSet.as_view({'get': 'retrieve'}))
]
