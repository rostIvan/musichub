from django.urls import path, include

__all__ = ['urlpatterns']

urlpatterns = [
    path('sign-up/', None),
    path('token/', include([
        path('obtain/', None),
        path('refresh/', None),
    ])),
]
