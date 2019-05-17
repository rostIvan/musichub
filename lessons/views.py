from rest_framework import viewsets

from lessons.models import Lesson
from lessons.paginators import LessonSetPagination
from lessons.serializers import LessonSerializer

__all__ = ['LessonViewSet']


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonSetPagination
