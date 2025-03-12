from django import forms
from .models import Comment



class CommentFrom(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    text = forms.CharField(required=False)
    widgets = {
        'text': forms.TextInput(attrs={'class': 'form-control'}),
    }