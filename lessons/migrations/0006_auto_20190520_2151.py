# Generated by Django 2.2.1 on 2019-05-20 21:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0005_auto_20190518_1813'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ('created',)},
        ),
    ]