from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import *
from django.contrib.auth import logout

from django.utils import timezone
from .models import Forum_categorie, Forum_topics, Forum_forum, Forum_post, User_profil, Topics_suivi

from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Count, F, Max

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token



from django.core.mail import EmailMessage


def profil_edit(request, id):
    post = get_object_or_404(User_profil, user=id)
    u=get_object_or_404(User, pk=id)
    if request.method == "POST":
        form = EditProfil(request.POST, request.FILES, instance=post)
        formuser=EditUser(request.POST,instance=u)
        if form.is_valid() and formuser.is_valid():
            post = form.save(commit=False)
            post.edit_date = timezone.now()

            post.save()
            p=formuser.save(commit=False)
            p.save()
            return redirect('profil', id=id)
    else:
        formuser=EditUser(instance=u)
        form = EditProfil(instance=post)
    return render(request, 'tutorial/profil_edit.html', {'form': form, 'formuser':formuser})

def profil(request, id):
    #infos = get_object_or_404(User_profil, user=id)
    profile = get_object_or_404(User, pk=id)
    return render(request, 'tutorial/profil.html', locals())

def home(request):
  categories = Forum_categorie.objects.order_by('order_place')
  listforum = Forum_forum.objects.all()


  forum_t = []

  for cat in categories:
    cat_forum = listforum.filter(categorie=cat)
    forum_t.append((cat, cat_forum))

  return render(request, 'tutorial/home.html', locals())

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            users = form.save(commit=False)
            users.is_active = False
            users.save()
            profil = User_profil(prenom=form.cleaned_data["prenom"], nom=form.cleaned_data["nom"], user=users)
            profil.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('tutorial/acc_active_email.html', {
                'user': users,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(users.pk)).decode(),
                'token': account_activation_token.make_token(users),
            })

            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()

            return render(request, 'tutorial/message_envoi.html', locals())
              #HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'tutorial/signup.html', {'form': form})


def activate(request, uidb64, token):
    message=""
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        users = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        users = None
    if users is not None and account_activation_token.check_token(users, token):
        users.is_active = True
        users.save()
        login(request, users)
        # return redirect('home')
        message="Votre adresse mail a été confirmé avec succes!"
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        message="Votre lien d'activation est invalide"
        #return HttpResponse('Activation link is invalid!')
    return render(request, 'tutorial/message_confirmation.html', locals())






def categorie(request, pk):

  uri=pk
  topics = []
  p = Forum_topics.objects.annotate(name_answer=Count('forum_post')).filter(forum_id=pk).order_by('-topic_date_create')
  topic = Forum_topics.objects.annotate(name_answer=Count('forum_post'), last_email=Max('forum_post__post_createur')).filter(forum_id=pk)
  for t in p:
    lastpost = Forum_post.objects.filter(topic_id=t).last()
    topics.append((t, lastpost ))

  listforum = get_object_or_404(Forum_forum, pk=pk)
  return render(request, 'tutorial/categorie.html', locals())

def categories(request, pk):
  forums=[]

  p = Forum_topics.objects.annotate(name_answer=Count('forum_post')).filter(categorie=pk).order_by('-topic_date_create')
  for t in p:
    lastpost = Forum_post.objects.filter(topic_id=t).last()
    forums.append((t, lastpost ))
  listforum = get_object_or_404(Forum_categorie, pk=pk)

  return render(request, 'tutorial/categories.html', locals())



def nouveau_sujet(request, pk):
  link = pk
  user = request.user
  listforum = get_object_or_404(Forum_forum, pk=pk)
  #form = PostForm()
  sujetform = TopicForm()
  if request.method == 'POST':
    #form = PostForm(request.POST)form.is_valid()
    sujetform = TopicForm(request.POST)

    if  sujetform.is_valid():
      title = sujetform.save(commit=False)
      title.forum_id = get_object_or_404(Forum_forum, pk=pk)
      title.topic_createur = user
      title.topic_last_post = 0
      title.topic_vu = 0
      title.categorie = listforum.categorie
      title.save()
      topic_suivi = Topics_suivi(sujet_suivi=title, user_suivi=user)
      topic_suivi.save()
      Forum_forum.objects.filter(pk=pk).update(last_post=title.id)
      Forum_topics.objects.filter(pk=title.id).update(topic_last_post=title.id)


      return redirect('categorie', pk=pk)
  return render(request, 'tutorial/test.html', locals())

def topics(request, uri, pk):
  Forum_topics.objects.filter(pk=pk).update(topic_vu=F('topic_vu')+1)
  fil =get_object_or_404(Forum_topics, pk=pk)
  comments = Forum_post.objects.filter(topic_id=pk)
  sujetform = TopicForm()
  form = PostForm()
  sujetsuivis = Topics_suivi.objects.filter(sujet_suivi=fil)
  if request.method == 'POST':
    form = PostForm(request.POST)
    user = request.user

    if form.is_valid():


      post = form.save(commit=False)
      post.post_createur = user
      post.topic_id = get_object_or_404(Forum_topics, pk=fil.id)
      post.forum_id = get_object_or_404(Forum_forum, pk=fil.forum_id.id)

      post.save()

      Forum_forum.objects.filter(pk=fil.forum_id.id).update(last_post=post.id)
      Forum_topics.objects.filter(pk=fil.id).update(topic_last_post=post.id)



      for s in sujetsuivis:
          current_site = get_current_site(request)
          mail_subject = 'Nouvelle réponse sur le topics "' + s.sujet_suivi.topic_titre+'" que vous suivez sur '+current_site.domain
          message = render_to_string('tutorial/reponse_topic_email.html', {
              'user': s.user_suivi,
              'domain': current_site.domain,
              'sujet' : s.sujet_suivi,
              'uri' : uri,
              'pk' : pk
            })
          to_email = s.user_suivi.email
          email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
          email.send()


      return redirect('topics', uri=uri, pk=pk)
  return render(request, 'tutorial/post.html', locals())
