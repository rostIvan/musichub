from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from lessons import swaggerdocs
from lessons.models import Lesson, Like
from lessons.paginators import LessonSetPagination
from lessons.serializers import LessonSerializer, LikeSerializer

__all__ = ['LessonViewSet']


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonSetPagination

    @swagger_auto_schema(**swaggerdocs.likes_get)
    @swagger_auto_schema(**swaggerdocs.likes_post)
    @action(methods=['GET', 'POST'], detail=True)
    def likes(self, request, pk=None):
        user = request.user
        if request.method == 'GET':
            return lesson_likes_json(lesson_id=pk, user_id=user.id)
        if request.method == 'POST':
            return toggle_user_like(lesson_id=pk, user_id=user.id)


def lesson_likes_json(lesson_id, user_id):
    try:
        who_likes = Lesson.get_users_who_likes(lesson_id)
    except Lesson.DoesNotExist:
        data = {'error': f"The lesson with id = {lesson_id} doesn't exist"}
        return Response(data, status.HTTP_404_NOT_FOUND)
    serializer = LikeSerializer((user_id, who_likes))
    return Response(serializer.data)


def toggle_user_like(lesson_id, user_id):
    if not user_id:
        data = {'error': 'You can not like something as anonymous user'}
        return Response(data, status.HTTP_401_UNAUTHORIZED)

    like, created = Like.objects.get_or_create(lesson_id=lesson_id,
                                               user_id=user_id)
    if not created:
        like.delete()
        return Response({'deleted': {'lesson': lesson_id}})
    else:
        data = {'like': {'user': like.user_id, 'lesson': like.lesson_id}}
        return Response(data, status.HTTP_201_CREATED)
