from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Category, Post, PostImages

class formPost(ModelForm):
    class Meta:
        model = Post
        fields = ['title','description', 'category']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class':'form-control', 'placeholder':'Enter a title'})
        self.fields['description'].widget.attrs.update({'class':'form-control', 'placeholder':'Enter a description'})
        self.fields['category'].widget.attrs.update({'class':'form-control', 'placeholder':'Select a category'})

        if user:            
            self.fields['category'].queryset = Category.objects.filter(user=user).order_by('name')

class formImage(ModelForm):
    class Meta:
        model = PostImages
        fields = ['post', 'images']

class formLoginUser(AuthenticationForm):
    class Meta:
        model = User  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control', 'placeholder':'Enter a username'})
        self.fields['password'].widget.attrs.update({'class':'form-control', 'placeholder':'Enter a password'})     

        
class formRegisterUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control', 'placeholder':'Enter a username'})
        self.fields['password1'].widget.attrs.update({'class':'form-control', 'placeholder':'Enter a password'})
        self.fields['password2'].widget.attrs.update({'class':'form-control', 'placeholder':'Confirm the password'})

