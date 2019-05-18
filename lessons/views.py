from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from lessons.models import Lesson
from lessons.paginators import LessonSetPagination
from lessons.serializers import LessonSerializer
from users.serializers import UserSerializer

__all__ = ['LessonViewSet']


def lesson_likes_json(lesson_id):
    try:
        who_likes = Lesson.get_users_who_likes(lesson_id)
    except Lesson.DoesNotExist:
        return Response(
            {'error': f"The lesson with id = {lesson_id} doesn't exist"},
            status.HTTP_404_NOT_FOUND
        )
    serializer = UserSerializer(who_likes, many=True)
    return Response({
        'count': len(who_likes),
        'users': serializer.data
    })


def toggle_user_like(lesson_id, user_id):
    raise NotImplementedError()


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonSetPagination

    @action(methods=['GET', 'POST'], detail=True)
    def likes(self, request, pk=None):
        if request.method == 'GET':
            return lesson_likes_json(lesson_id=pk)
        if request.method == 'POST':
            return toggle_user_like(lesson_id=pk, user_id=request.user.id)
