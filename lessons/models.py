from django.contrib.auth import get_user_model
from django.db import models

__all__ = ['Lesson', 'Like']


class Lesson(models.Model):
    title = models.CharField(max_length=155)
    user = models.ForeignKey(get_user_model(), related_name='lessons',
                             on_delete=models.SET_NULL, null=True, blank=False)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'lessons'

    def __str__(self):
        return f'{self.id} | {self.user.name} | {self.text[:20]}'


class Like(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='likes',
                             on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='likes',
                               on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'
        unique_together = ("user", "lesson")

    def __str__(self):
        return f'{self.id} | {self.user.email} | {self.lesson.title}'
