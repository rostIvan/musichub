from rest_framework import serializers
from rest_framework.reverse import reverse

from lessons.models import Lesson, Like
from users.serializers import UserSerializer


class LessonSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    likes_link = serializers.SerializerMethodField()

    def get_likes_count(self, instance):
        return Like.objects.filter(lesson_id=instance.id).count()

    def get_likes_link(self, instance):
        request = self.context['request']
        sub_link = reverse('lesson_likes', args=(instance.id,))
        return request.build_absolute_uri(sub_link)

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'text', 'created', 'user',
                  'likes_count', 'likes_link')
        read_only_fields = ('id', 'created', 'user',
                            'likes_count', 'likes_link')


class AuthLessonSerializer(LessonSerializer):
    like = serializers.SerializerMethodField('is_already_like')

    def is_already_like(self, instance):
        user = self.context['request'].user
        return Like.objects.filter(lesson=instance, user=user).exists()

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'text', 'created', 'user',
                  'like', 'likes_count', 'likes_link')
        read_only_fields = ('id', 'created', 'user', 'like',
                            'likes_count', 'likes_link')


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Like
        fields = ('id', 'user')
        read_only_fields = ('id', 'user')
