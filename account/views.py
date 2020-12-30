from django.shortcuts import render
from django.views.generic import CreateView
from account.models import CustomUser
from account.forms import RegisterForm

# Create your views here.

User=CustomUser

class RegisterView(CreateView):
    template_name='register.html'
    model=User
    form_class=RegisterForm
    success_url='/'

