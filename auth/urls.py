from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from auth.views import SignUpView, AccountActivationView

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('activate-account/<uuid>',
         AccountActivationView.as_view(), name='activate_account'),

    path('token/', include([
        path('obtain/', TokenObtainPairView.as_view(), name='token_obtain'),
        path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ])),
]
