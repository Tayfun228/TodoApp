from django.urls import path, include
from django.contrib.auth.views import LogoutView
from account.views import *

urlpatterns = [
    path('login/', CustomLoginView.as_view(template_name='login.html'),name='login'),
    path('register/', RegisterView.as_view(),name='register'),

]