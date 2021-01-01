from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from home.views import HomeView, ToDoView,TaskDetailView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', HomeView.as_view(),name='home'),
    path('todo/', ToDoView.as_view(),name='todo'),
    path('task/<int:pk>/', TaskDetailView.as_view(),name='task-detail'),


    # path('', LoginView.as_view(template_name='login.html'),name='login'),

]