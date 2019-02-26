from django.conf.urls import url
from django.urls import path

from . import views


urlpatterns = [
  # /tutorial

  path('', views.home, name="home"),

  path('profil/<id>', views.profil, name="profil"),
  path('nouveau/message/<id>', views.send_messages, name="send_messages"),
  path('messages/<id>', views.messages, name="message"),
  path('notifications/<id>', views.notifications, name="notifications"),
  path('view_notification/<id>', views.view_notification, name="view_notification"),

  path('profil/edit/<id>', views.profil_edit, name="profil_edit"),
  path('categorie/<pk>', views.categorie, name="categorie"),

  path('nouveau_sujet/<pk>', views.nouveau_sujet, name="nouveau_sujet"),
  path('topics/<uri>/<pk>', views.topics, name="topics"),
  path('categories/<pk>', views.categories, name="categories"),
  url(r'^signup/$', views.signup, name='signup'),
  url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
  path('voir_message/<id>', views.voir_message, name="voir_message")
]
