from django.contrib.auth import get_user_model
from django.db import models

__all__ = ['Lesson', 'Like']


class Lesson(models.Model):
    title = models.CharField(max_length=155)
    user = models.ForeignKey(get_user_model(), related_name='lessons',
                             on_delete=models.SET_NULL, null=True, blank=False)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_users_who_likes(lesson_id: int) -> list:
        likes = (Lesson.objects.get(id=lesson_id)
                 .likes
                 .select_related('user')
                 .defer('lesson'))
        who_likes = [like.user for like in likes]
        return who_likes

    def __str__(self):
        return f'{self.id} | {self.user.email} | {self.text[:20]}'

    class Meta:
        db_table = 'lessons'
        ordering = ('created',)


class Like(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='likes',
                             on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='likes',
                               on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} | {self.user.email} | {self.lesson.title}'

    class Meta:
        db_table = 'likes'
        unique_together = ("user", "lesson")
