from django import forms
from django.forms import ModelForm, modelformset_factory, ClearableFileInput

from .models import Post, PostAttachment

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('body', 'is_private', 'journeyid', 'label',) 


class AttachmentForm(ModelForm):
    class Meta:
        model = PostAttachment
        fields = ('file',)
        #widgets = {
        #    'file': forms.ClearableFileInput(attrs={'multiple': True}),
        #}

AttachmentFormSet = modelformset_factory(
    PostAttachment, fields = ('file',)
)