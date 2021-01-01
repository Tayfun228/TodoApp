from django.shortcuts import render
from django.views.generic import CreateView
from account.models import CustomUser,LoginHistory
from account.forms import RegisterForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect

# Create your views here.

User=CustomUser

class RegisterView(CreateView):
    template_name='register.html'
    model=User
    form_class=RegisterForm
    success_url='/'

class CustomLoginView(LoginView):
    def get_success_url(self):
        try:
            user=self.request.user
            ip=self.visitor_ip_address(self.request)
            browser = self.request.user_agent.browser.family  # returns 'Mobile Safari'
            os = self.request.user_agent.os.family  # returns 'iOS'
            device= self.request.user_agent.device.family  # returns Device(family='iPhone')
            print(user,ip,browser,os,device)
            history=LoginHistory(user=user,ip=ip,browser=browser,os=os,device=device)
            history.save()
        except:
            pass
        return super().get_success_url()
    
    def visitor_ip_address(self,request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


    # def form_valid(self, form):
    #     """If the form is valid, save the associated model."""
    #     self.object = form.save()
    #     print(form)
    #     print(form.data)
    #     print(form.data['email'])
    #     user=self.model.objects.filter(email=form.data['email']).first()
    #     print(user)

        
    #     return HttpResponseRedirect(self.get_success_url())
    #     # return super().form_valid(form)

