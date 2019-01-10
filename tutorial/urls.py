from django.urls import path

from . import views


urlpatterns = [
  # /tutorial
  path('', views.home, name='home'),
  path('signin', views.sign_in, name='signin'),
  path('callback', views.callback, name='callback'),
  path('signout', views.sign_out, name='signout'),
  path('categorie/<pk>', views.categorie, name="categorie"),
  path('test', views.test, name="test"),
  path('nouveau_sujet/<pk>', views.nouveau_sujet, name="nouveau_sujet")
]