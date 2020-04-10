from django import forms
from django.contrib.auth.models import User

class MyProfile(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(MyProfile, self).__init__(*args, **kwargs)
        try:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
        except:
            pass
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')