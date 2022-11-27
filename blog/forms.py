from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=500, widget=forms.Textarea(attrs={
        "class": "form-control",
        "rows": 3,
        "placeholder": "Join the discussion and leave a comment!"
    }))

    class Meta:
        model = Comment
        fields = ['comment']
