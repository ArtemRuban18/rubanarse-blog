from django import forms
from django.forms import ModelForm
from .models import Post, Category,Comment
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from taggit.models import Tag

class CreatePostForm(forms.ModelForm):
    """
    Form for create new posts

    Fields:
        - title: CharField
        - category: ChoiceField
        - content: CharField
    """
    
    content = forms.CharField(widget=CKEditorWidget)
    class Meta:
        model = Post
        fields = ['title','category', 'content']
        labels = {
            'title':'Заголовок',
            'category':'Категорія',
            'content':'Текст',
        }

    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        
        categories = Category.objects.all()
        if categories.exists():
            self.fields['category'].empty_label = None
            self.fields['category'].initial = categories.first()

class CommentForm(forms.ModelForm):
    """
    Form for post comments

    Fields:
        - comment: CharFiled
    """

    class Meta:
        model = Comment
        fields = ['comment']

