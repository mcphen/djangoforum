from django import forms
from froala_editor.widgets import FroalaEditor
from .models import Forum_post, Forum_topics, User_profil
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EditUser(forms.ModelForm):
    class Meta:
        model=User
        fields=('username',)


class EditProfil(forms.ModelForm):
    class Meta:
        model=User_profil
        fields=('avatar','prenom','nom','description_user','date_naissance','tel','site_web','facebook', 'linkedin','biographie')

    def __init__(self, *args, **kwargs):
        super(EditProfil, self).__init__(*args, **kwargs)
        self.fields['avatar'].required = False
        self.fields['prenom'].required = False
        self.fields['nom'].required = False
        self.fields['description_user'].required = False
        self.fields['date_naissance'].required = False
        self.fields['tel'].required = False
        self.fields['site_web'].required = False
        self.fields['facebook'].required = False
        self.fields['linkedin'].required = False
        self.fields['biographie'].required = False
  
class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    nom = forms.CharField(max_length=200, help_text='Required')
    prenom = forms.CharField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username','nom','prenom', 'email', 'password1', 'password2')

class TopicForm(forms.ModelForm):

    class Meta:
        model=Forum_topics
        fields=('topic_titre','content')

    def __init__(self, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        self.fields['topic_titre'].label = "sujet"
        self.fields['content'].label = "Message"

class PostForm(forms.ModelForm):

    class Meta:
        model=Forum_post
        fields=('post_texte',)

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['post_texte'].label = "Message"
