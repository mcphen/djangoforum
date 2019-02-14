from django import forms
from froala_editor.widgets import FroalaEditor
from .models import Forum_post, Forum_topics
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

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
