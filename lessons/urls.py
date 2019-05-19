from rest_framework import routers

from lessons.views import LessonViewSet

router = routers.SimpleRouter()
router.register('', LessonViewSet, 'lessons')
urlpatterns = router.urls
