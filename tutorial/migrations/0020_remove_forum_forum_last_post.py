# Generated by Django 2.1.4 on 2019-02-26 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0019_auto_20190226_1234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forum_forum',
            name='last_post',
        ),
    ]
