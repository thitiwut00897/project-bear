from django import forms
from django.contrib.auth.models import User
from main.models import *
class ProfileForm(forms.ModelForm):
    picture = forms.ImageField()
    class Meta:
        model = Profile
        fields = ('tel','picture')

class UpdateProfile(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
class ProductForm(forms.ModelForm):
    price = forms.FloatField(required=True)
    picture = forms.ImageField(label='Picture',required=True)
    class Meta:
        model = Product
        fields = "__all__"