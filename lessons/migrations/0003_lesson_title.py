# Generated by Django 2.2.1 on 2019-05-16 22:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0002_lesson_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='title',
            field=models.CharField(default=django.utils.timezone.now, max_length=155),
            preserve_default=False,
        ),
    ]