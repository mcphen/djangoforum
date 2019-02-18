from django.contrib import admin

from .models import Forum_categorie, Forum_topics, Forum_forum, Forum_post, User_profil, Topics_suivi

# Register your models here.
admin.site.register(Forum_post)
admin.site.register(Forum_forum)
admin.site.register(Forum_topics)
admin.site.register(Forum_categorie)
admin.site.register(User_profil)
admin.site.register(Topics_suivi)
