from django.db import models

# Create your models here.
from django.utils import timezone
from tinymce.models import HTMLField


class Forum_categorie(models.Model):
    categorie_nom = models.CharField(max_length=255)

    def __str__(self):
        return self.categorie_nom

class Forum_forum(models.Model):
    forum_nom =  models.CharField(max_length=255)
    forum_description = models.TextField()
    categorie = models.ForeignKey(Forum_categorie, on_delete=models.CASCADE)
    last_post = models.IntegerField(default=None)
    logo_forum = models.ImageField(upload_to="photos/")
    forum_actived = models.IntegerField()

    def __str__(self):
        return self.forum_nom

class Forum_topics(models.Model):
    topic_titre = models.CharField(max_length=255)
    forum_id = models.ForeignKey(Forum_forum,on_delete=models.CASCADE )
    topic_createur = models.CharField(max_length=255)
    topic_last_post=models.IntegerField(default=None)
    topic_vu = models.IntegerField(default=None)
    topic_date_create = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.topic_titre

class Forum_post(models.Model):
    post_texte = HTMLField()
    post_createur = models.CharField(max_length=255)
    post_date_create =  models.DateTimeField(default=timezone.now)
    topic_id = models.ForeignKey(Forum_topics,on_delete=models.CASCADE )
    forum_id = models.ForeignKey(Forum_forum,on_delete=models.CASCADE )



