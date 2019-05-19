from rest_framework import serializers

from lessons.models import Lesson
from users.serializers import UserSerializer

__all__ = ['LessonSerializer', 'LikeSerializer']


class LessonSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'text', 'created', 'user',)
        read_only_fields = ('id', 'created', 'user')


class LikeSerializer(serializers.Serializer):
    count = serializers.SerializerMethodField('get_likes_count')
    liked = serializers.SerializerMethodField('is_liked_by_user')
    users = serializers.SerializerMethodField('get_liked_users')

    @staticmethod
    def get_likes_count(instance: tuple) -> int:
        _, who_likes = instance
        return len(who_likes)

    @staticmethod
    def is_liked_by_user(instance: tuple) -> bool:
        user_id, who_likes = instance
        return user_id in [user.id for user in who_likes]

    @staticmethod
    def get_liked_users(instance: tuple) -> dict:
        _, who_likes = instance
        return UserSerializer(who_likes, many=True).data
