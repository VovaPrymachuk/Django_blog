from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Post, Tag


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'tags']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Post title..'}),
            'slug': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Slug must be unique'}),
            'body': forms.Textarea(attrs={'class': 'form-control',
                                          'placeholder': 'Post body..'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control',
                                                'label': 'Select tag'})
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('Slug may not be "create".')
        return new_slug


class TagCreateForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['title', 'slug']

        widgets = {
            'title': forms.TextInput(),
            'slug': forms.TextInput()
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('Slug may not be "create".')
        if Tag.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError('Slug must be unique.')
        return new_slug
