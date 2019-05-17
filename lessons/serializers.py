from rest_framework import serializers

from lessons.models import Lesson

__all__ = ['LessonSerializer']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'text', 'created', 'user')
