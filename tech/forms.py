from django import forms
from .models import Post, Comment, Bug
from django_summernote.widgets import SummernoteWidget

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["photo", "caption"]
        widgets = {
            "caption": SummernoteWidget(attrs={'summernote': {'width': '500px', 'height': '500px'}}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 4}),
        }

class BugReportForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = ('title', 'category', 'description', 'image',)

