from django import forms
from django.contrib.auth.models import User
from main.models import *
class ProfileForm(forms.ModelForm):
    tel = forms.CharField(max_length=10,widget=forms.TextInput(attrs={'class':'form-control'}))
    picture = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}),required=False)
    class Meta:
        model = Profile
        fields = ('tel','picture')

class UpdateProfile(forms.ModelForm):
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
class ProductForm(forms.ModelForm):
    description = forms.CharField(required=False)
    price = forms.DecimalField(required=True)
    stock = forms.IntegerField(min_value=0)
    picture = forms.ImageField(label='Picture',required=False)
    class Meta:
        model = Product
        fields = "__all__"