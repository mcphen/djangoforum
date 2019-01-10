from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import *

from .graph_helper import get_user
from .auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, remove_user_and_token

from .models import Forum_categorie, Forum_topics, Forum_forum, Forum_post

from django.http import HttpResponse, HttpResponseRedirect

def initialize_context(request):
  context = {}

  # Check for any errors in the session
  error = request.session.pop('flash_error', None)

  if error != None:
    context['errors'] = []
    context['errors'].append(error)

  # Check for user in the session
  context['user'] = request.session.get('user', {'is_authenticated': False})
  return context

def home(request):
  context = initialize_context(request)

  categories = Forum_categorie.objects.all()
  listforum = Forum_forum.objects.all()


  forum_t = []

  for cat in categories:
    cat_forum = listforum.filter(categorie=cat)

    forum_t.append((cat, cat_forum))

  return render(request, 'tutorial/home.html', context)

def sign_in(request):
  # Get the sign-in URL
  sign_in_url, state = get_sign_in_url()
  # Save the expected state so we can validate in the callback
  request.session['auth_state'] = state
  # Redirect to the Azure sign-in page
  return HttpResponseRedirect(sign_in_url)

def callback(request):
  # Get the state saved in session
  expected_state = request.session.pop('auth_state', '')
  # Make the token request
  token = get_token_from_code(request.get_full_path(), expected_state)

  # Get the user's profile
  user = get_user(token)

  # Save token and user
  store_token(request, token)
  store_user(request, user)

  return HttpResponseRedirect(reverse('home'))

def sign_out(request):
  # Clear out the user and token
  remove_user_and_token(request)

  return HttpResponseRedirect(reverse('home'))


def categorie(request, pk):
  url=pk
  topics = Forum_topics.objects.filter(forum_id=pk)
  listforum = get_object_or_404(Forum_forum, pk=pk)
  return render(request, 'tutorial/categorie.html', locals())


def test(request):


  return render(request, 'tutorial/test1.html', locals())

def nouveau_sujet(request, pk):
  link = pk
  user = request.user
  listforum = get_object_or_404(Forum_forum, pk=pk)
  form = PostForm()
  sujetform = TopicForm()
  if request.method == 'POST':
    form = PostForm(request.POST)
    sujetform = TopicForm(request.POST)

    if form.is_valid() and sujetform.is_valid():
      title = sujetform.save(commit=False)
      title.forum_id = get_object_or_404(Forum_forum, pk=pk)
      title.topic_createur = user.email
      title.topic_last_post = 0
      title.topic_vu = 0
      title.save()

      post = form.save(commit=False)
      post.post_createur = user.email
      post.topic_id = get_object_or_404(Forum_topics, pk=title.id)
      post.forum_id = get_object_or_404(Forum_forum, pk=pk)

      post.save()

      Forum_forum.objects.filter(pk=pk).update(last_post=post.id)
      Forum_topics.objects.filter(pk=title.id).update(topic_last_post=post.id)

      return redirect('categorie', pk=pk)
  return render(request, 'tutorial/test.html', locals())

def topics(request, uri, pk):
  posts = Forum_post.objects.filter(categorie=pk)
  return render(request, 'tutorial/post.html', locals())