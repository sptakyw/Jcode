from django import forms
from .models import Video,VideoChapter,VideoLesson

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        exclude = ['id','member', 'slug', 'published', 'created', 'updated']

class VideochapterForm(forms.ModelForm):
    class Meta:
        model = VideoChapter
        exclude = ['id', 'created', 'updated']

class VideolessonForm(forms.ModelForm):
    class Meta:
        model = VideoLesson
        exclude = ['id', 'created', 'updated']
