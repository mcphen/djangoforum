from datetime import date

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db.models import Q
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
    topic_last_post=models.ForeignKey('Forum_post', related_name='last_post', blank=True, null=True, on_delete=models.CASCADE)
    #topic_vu = models.IntegerField(default=None)
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

    def get_notifmessage(self):
        user_profile = Reponse.objects.filter(destinateur=self.user, is_readed=False).count()
        return user_profile
    def get_notifications(self):
        user_profile = Notifications.objects.filter(Q(user=self.user), Q(is_readed=False)).count()
        return user_profile

class Topics_suivi(models.Model):
    sujet_suivi = models.ForeignKey(Forum_topics, on_delete=models.CASCADE)
    user_suivi =  models.ForeignKey(User,on_delete=models.CASCADE)

"""
class TopicView(models.Model):
    topic = models.ForeignKey(Forum_topics, on_delete=models.CASCADE)
    adress_ip = models.GenericIPAddressField()
    date_visit=models.DateField(default=date.today)

class VisitSite(models.Model):
    adress_ip = models.GenericIPAddressField()
    date_visit=models.DateField(default=date.today)"""

class MessageUser(models.Model):
    titre_message=models.CharField(max_length=255, null=True)
    #message= HTMLField()
    #pub_date = models.DateTimeField(default=timezone.now)

    last_message = models.ForeignKey('Reponse', related_name='last_answer', blank=True, null=True, on_delete=models.CASCADE)



    def __str__(self):
        return self.titre_message
class Reponse(models.Model):
    title = models.ForeignKey(MessageUser, on_delete=models.CASCADE)
    expediteur = models.ForeignKey(User_profil, on_delete=models.CASCADE)
    destinateur = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_message = HTMLField()
    answer_date =  models.DateTimeField(default=timezone.now)

    is_readed = models.BooleanField(default=False)

    #answer_user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering=['answer_date']

    def __str__(self):
        return self.answer_message


class Notifications(models.Model):
    topic = models.ForeignKey(Forum_topics, on_delete=models.CASCADE)
    is_readed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
