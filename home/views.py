from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView, TemplateView, ListView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Task, Share
from home.tasks import *


# Create your views here.


class HomeView(TemplateView):
    template_name='home.html'

    def get(self, request, *args, **kwargs):
        print("YEAH BOY")
        # expired_at.delay()
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('todo'))
            
        else:
            # self.template_name='login.html'
            return HttpResponseRedirect(reverse_lazy('login'))

        return super(HomeView, self).get(request, *args, **kwargs)

class ToDoView(LoginRequiredMixin, ListView):
    template_name='todo.html'
    queryset=[]
    context_object_name = 'objects'

    def get_queryset(self): 
        self.queryset = Task.objects.filter(user=self.request.user)
        return self.queryset 

class TaskDetailView(LoginRequiredMixin, DetailView):
    template_name='task-detail.html'
    model=Task

    def get(self, request, *args, **kwargs):
        id=kwargs['pk']
        self.id=id
        task=Task.objects.get(id=id)
        user=request.user
        print(task)
        print(user)
        print(Share.objects.all())
        print(Share.objects.filter(user=user, task=task))
        if Share.objects.filter(user=user, task=task) or task.user == user:
            return super(TaskDetailView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy('todo'))

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        context['room_name'] = self.id
        return context
        # if request.user.is_authenticated:
        #     return HttpResponseRedirect(reverse_lazy('todo'))
    # context_object_name = 'objects'
    # query_pk_and_slug='id'
    
    # def get_queryset(self): 
    #     self.queryset = Task.objects.filter(user=self.request.user)
    #     return self.queryset 

    # def dispatch(self, request, *args, **kwargs):
    #     # print(self.kwargs['id'])
    #     # id=self.kwargs['id']
    #     # task=Task.objects.get(id=id)
    #     # print(tasks)

    #     return super(TaskDetailView, self).dispatch(request, *args, **kwargs)

   