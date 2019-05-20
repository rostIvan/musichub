from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from lessons.models import Lesson, Like
from lessons.serializers import LessonSerializer, LikeSerializer
from musichub.paginators import DefaultSetPagination


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = DefaultSetPagination


class LikeViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    pagination_class = DefaultSetPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        lesson = self.get_lesson_or_404()
        return Like.objects.filter(lesson=lesson)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return LikeSerializer
        if self.request.method == 'POST':
            return Serializer
        return super().get_serializer_class()

    @action(methods=['POST'], detail=False)
    def toggle(self, *_args, **_kwargs):
        lesson = self.get_lesson_or_404()
        like, created = Like.objects.get_or_create(user=self.request.user,
                                                   lesson=lesson)
        if not created:
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(LikeSerializer(like).data, status.HTTP_200_OK)

    def get_lesson_or_404(self):
        return get_object_or_404(Lesson, id=self.kwargs['lesson_id'])
