from rest_framework import serializers

from lessons.models import Lesson, Like
from users.serializers import UserSerializer


class LessonSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'text', 'created', 'user')
        read_only_fields = ('id', 'created', 'user')


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Like
        fields = ('id', 'user')
        read_only_fields = ('id', 'user')
