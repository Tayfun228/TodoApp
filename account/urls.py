from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from account.views import *

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'),name='login'),
    path('register/', RegisterView.as_view(),name='register'),

]