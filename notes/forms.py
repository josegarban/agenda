from django import forms
from taggit.forms import *
from .models import Post
from django.utils.translation import ugettext_lazy as _

class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={  'class':'input',
                                                            'type': 'text',
                                                            'style': 'padding=2rem;',
                                                            'placeholder': 'Title',
                                                            }))
    status = forms.ChoiceField( widget=forms.Select(attrs={'class':'select',
                                                            'style': 'padding=2rem;',
                                                            }),
                                choices=Post.STATUS_CHOICES,
                                )
    # tags = TagField()

    class Meta:
        model = Post
        fields = ('title', 'text', 'status', 'tasks', 'tags')
        exclude = ('published_date', 'created_date')
        labels = {
            'title': _('title'),
            'text': _('text'),
            'status': _('status'),
            'tags': _('tags'),
            'tasks': _('tasks'),
        }


class EmailPostForm(forms.Form):
    name     = forms.CharField (max_length=30)
    email    = forms.EmailField()
    to       = forms.EmailField()
    comments = forms.CharField (required=False,
                                widget=forms.Textarea)


# class CommentForm(forms.ModelForm):
#     name = forms.CharField(widget=forms.TextInput(attrs={  'class':'input',
#                                                             'type': 'text',
#                                                             'style': 'width:40%;',
#                                                             'placeholder': 'Name',
#                                                             'help_text':None,
#                                                             }))
#     body = forms.CharField(widget=forms.Textarea(attrs={  'class':'input',
#                                                             'type': 'text',
#                                                             'style': 'width:70%;height:8rem;',
#                                                             'placeholder': 'Your text',
#                                                             'help_text':None,
#                                                             }))
#
#     class Meta:
#         model = Comment
#         fields = ('name', 'body')
