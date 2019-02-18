from django.conf.urls import url
from django.urls import path

from . import views


urlpatterns = [
  # /tutorial
 # path('home', views.home, name='home'),
  path('', views.home, name="home"),
  #path('signin', views.sign_in, name='signin'),
  #path('callback', views.callback, name='callback'),
  path('profil/<id>', views.profil, name="profil"),
  path('profil/edit/<id>', views.profil_edit, name="profil_edit"),
  path('categorie/<pk>', views.categorie, name="categorie"),
  #path('test', views.test, name="test"),
  path('nouveau_sujet/<pk>', views.nouveau_sujet, name="nouveau_sujet"),
  path('topics/<uri>/<pk>', views.topics, name="topics"),
  path('categories/<pk>', views.categories, name="categories"),
  url(r'^signup/$', views.signup, name='signup'),
  url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
