from rest_framework import serializers
from rest_framework.reverse import reverse

from lessons.models import Lesson, Like
from users.serializers import UserSerializer


class LessonSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    likes_link = serializers.SerializerMethodField()

    def get_likes_link(self, instance):
        request = self.context['request']
        sub_link = reverse('lesson_likes', args=(instance.id,))
        return request.build_absolute_uri(sub_link)

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'text', 'created', 'user', 'likes_link')
        read_only_fields = ('id', 'created', 'user')


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Like
        fields = ('id', 'user')
        read_only_fields = ('id', 'user')
