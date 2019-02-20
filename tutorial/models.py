from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.utils import timezone
from tinymce.models import HTMLField


class Forum_categorie(models.Model):
    categorie_nom = models.CharField(max_length=255)
    order_place = models.IntegerField()

    def __str__(self):
        return self.categorie_nom

class Forum_forum(models.Model):
    forum_nom =  models.CharField(max_length=255)
    forum_description = models.TextField()
    categorie = models.ForeignKey(Forum_categorie, on_delete=models.CASCADE)
    last_post = models.ForeignKey('Forum_post', related_name='last_forum_post', blank=True, null=True, on_delete=models.CASCADE)
    logo_forum = models.ImageField(upload_to="photos/")
    forum_actived = models.IntegerField()

    def __str__(self):
        return self.forum_nom

class Forum_topics(models.Model):
    topic_titre = models.CharField(max_length=255)
    forum_id = models.ForeignKey(Forum_forum,on_delete=models.CASCADE )
    topic_createur = models.ForeignKey(User,on_delete=models.CASCADE)
    topic_last_post=models.IntegerField(default=None)
    topic_vu = models.IntegerField(default=None)
    topic_date_create = models.DateTimeField(default=timezone.now)
    content = HTMLField()
    categorie = models.ForeignKey(Forum_categorie, on_delete=models.CASCADE)

    def __str__(self):
        return self.topic_titre

class Forum_post(models.Model):
    post_texte = HTMLField()
    post_createur = models.ForeignKey(User,on_delete=models.CASCADE)
    post_date_create =  models.DateTimeField(default=timezone.now)
    topic_id = models.ForeignKey(Forum_topics,on_delete=models.CASCADE )
    forum_id = models.ForeignKey(Forum_forum,on_delete=models.CASCADE )
    #p_categorie = models.ForeignKey(Forum_categorie, on_delete=models.CASCADE)


class User_profil(models.Model):
    user   = models.OneToOneField(User,on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatar/', null=True)
    description_user= models.CharField(max_length=255,  null=True)
    prenom = models.CharField(max_length=255, null=True)
    nom  = models.CharField(max_length=255, null=True)
    date_naissance =  models.DateTimeField( null=True)
    #sexe = models.CharField(max_length=2, null=True)
    tel = models.CharField(max_length=55, null=True)
    site_web = models.URLField(max_length=255, null=True)
    facebook = models.URLField(max_length=255, null=True)
    linkedin = models.URLField(max_length=255, null=True)
    biographie= HTMLField( null=True)
    edit_date=models.DateTimeField(
        blank=True, null=True)

class Topics_suivi(models.Model):
    sujet_suivi = models.ForeignKey(Forum_topics, on_delete=models.CASCADE)
    user_suivi =  models.ForeignKey(User,on_delete=models.CASCADE)
