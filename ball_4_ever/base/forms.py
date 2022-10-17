from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['answer']

        widgets = {
            'answer': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Your Answer"})
        }