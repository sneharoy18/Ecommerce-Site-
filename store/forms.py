from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms



from .models import Order


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


    def clean_email(self):                   #through this we can validate any data
        email = self.cleaned_data.get("email")
        email_exist = User.objects.filter(email=email)
        if email_exist :
            raise forms.ValidationError("This email already exist Please login")
        return email
