from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ClearableFileInput
from . import models
from .models import Profile,Product,Comment

class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email']

class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['name','avatar','about','country','county','location','phone','whatsapp','facebook','instagram']

class CreateProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name','category','brand','location','thumbnail','thumbnail1','thumbnail2','price','description','slug','instock', 'promoted']
        widgets = {
            'thumbnail': ClearableFileInput(attrs={'multiple': True}),
        }

class CreateCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['body']