from django import forms
from froala_editor.widgets import FroalaEditor
from .models import Forum_post, Forum_topics

class TopicForm(forms.ModelForm):

    class Meta:
        model=Forum_topics
        fields=('topic_titre',)

    def __init__(self, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        self.fields['topic_titre'].label = "sujet"

class PostForm(forms.ModelForm):

    class Meta:
        model=Forum_post
        fields=('post_texte',)

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['post_texte'].label = "Message"
