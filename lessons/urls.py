from django.urls import path
from rest_framework import routers

from lessons.views import LessonViewSet, LikeViewSet

router = routers.SimpleRouter()
router.register('', LessonViewSet, 'lessons')

urlpatterns = [
    path('<lesson_id>/likes/',
         LikeViewSet.as_view({'get': 'list', 'post': 'toggle'}),
         name='lesson_likes'),
]

urlpatterns += router.urls
