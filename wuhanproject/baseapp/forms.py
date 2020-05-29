from django import forms
from baseapp.models import *
from ckeditor.widgets import CKEditorWidget

# ---------------------------------------------------------------------------------


class PostForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())
    nickname = forms.CharField()

    class Meta:
        model = Post