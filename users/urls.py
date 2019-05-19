from rest_framework import routers

from users.views import UserViewSet

router = routers.SimpleRouter()
router.register('', UserViewSet, 'users')
urlpatterns = router.urls
