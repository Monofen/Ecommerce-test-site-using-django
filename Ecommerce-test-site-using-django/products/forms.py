from django import forms
from .models import Rating, Comment

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['stars', 'comment', 'image']
        widgets = {
            'stars': forms.RadioSelect(choices=[
                (1, '1 Star'),
                (2, '2 Stars'),
                (3, '3 Stars'),
                (4, '4 Stars'),
                (5, '5 Stars')
            ]),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }
