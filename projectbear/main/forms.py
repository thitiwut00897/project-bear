from django import forms
from django.contrib.auth.models import User
from main.models import *
class ProfileForm(forms.ModelForm):
    tel = forms.CharField(label='เบอร์มือถือ',max_length=10,widget=forms.TextInput(attrs={'class':'form-control'}))
    picture = forms.ImageField(label='รูปภาพของผู้ใช้',widget=forms.FileInput(),required=False)
    class Meta:
        model = Profile
        fields = ('tel','picture')

class UpdateProfile(forms.ModelForm):
    username = forms.CharField(label='ชื่อผู้ใช้',required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='อีเมล',required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(label='ชื่อจริง',required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label='นามสกุล',required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
class ProductForm(forms.ModelForm):
    type = forms.ModelChoiceField(queryset=Type.objects.all(),label='ประเภทสินค้า')
    name = forms.CharField(label='ชื่อสินค้า',required=True)
    description = forms.CharField(label='คำอธิบาย',required=False)
    price = forms.DecimalField(label='ราคา',required=True,min_value=0)
    stock = forms.IntegerField(label='จำนวนสินค้าในคลัง',min_value=0)
    picture = forms.ImageField(label='รูปภาพของสินค้า',widget=forms.FileInput(),required=False)
    class Meta:
        model = Product
        fields = "__all__"