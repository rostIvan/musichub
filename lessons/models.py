from django.contrib.auth import get_user_model
from django.db import models

__all__ = ['Lesson']

User = get_user_model()


class Lesson(models.Model):
    user = models.ForeignKey(User, related_name='lessons',
                             on_delete=models.SET_NULL, null=True, blank=False)
    text = models.TextField(blank=False, null=False)

    def __str__(self):
        return f'{self.id} | {self.user.name} | {self.text[:20]}'

    class Meta:
        db_table = 'lessons'
