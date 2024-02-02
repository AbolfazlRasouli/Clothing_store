from django import forms
from .models import Comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', 'reply_comment')
        widgets = {
            'body': forms.Textarea(attrs={'cols': 100, 'rows': 10, 'placeholder': 'نظر خود را وارد کنید...'}),
        }
