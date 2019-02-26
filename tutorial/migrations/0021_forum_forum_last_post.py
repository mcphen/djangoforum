# Generated by Django 2.1.4 on 2019-02-26 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0020_remove_forum_forum_last_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum_forum',
            name='last_post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='last_forum_post', to='tutorial.Forum_post'),
        ),
    ]