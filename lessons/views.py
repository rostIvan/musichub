from django.http import Http404
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from lessons.models import Lesson, Like
from lessons.serializers import (LikeSerializer, AuthLessonSerializer,
                                 LessonSerializer)
from musichub.paginators import DefaultSetPagination
from musichub.permissions import IsOwnerOrReadOnly, IsAuthForCreation


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    pagination_class = DefaultSetPagination
    permission_classes = (IsOwnerOrReadOnly, IsAuthForCreation)

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return AuthLessonSerializer
        return LessonSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    pagination_class = DefaultSetPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = LikeSerializer

    def get_queryset(self):
        lesson = self.get_lesson_or_404()
        return Like.objects.filter(lesson=lesson)

    @swagger_auto_schema(
        method='POST',
        operation_description="Send POST for this route can `toggle` "
                              "like on lesson with {lesson_id}",
        request_body=Serializer,
        responses={
            201: 'Like created',
            204: 'Like deleted',
            404: 'Lesson with {lesson_id} not found',
        })
    @action(methods=['POST'], detail=False)
    def toggle(self, *args, **kwargs):
        lesson = self.get_lesson_or_404()
        like, created = Like.objects.get_or_create(user=self.request.user,
                                                   lesson=lesson)
        if not created:
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(LikeSerializer(like).data, status.HTTP_201_CREATED)

    def get_lesson_or_404(self):
        try:
            lesson_id = int(self.kwargs['lesson_id'])
        except ValueError:
            raise Http404()
        return get_object_or_404(Lesson, id=lesson_id)
