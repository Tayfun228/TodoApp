from django.contrib.auth.forms import UserCreationForm
from django import forms
from account.models import CustomUser

class RegisterForm(UserCreationForm):
    # email = forms.EmailField(label = "Email")
    # fullname = forms.CharField(label = "First name")
    class Meta:
        model = CustomUser
        fields = ("first_name","last_name","email","username")
