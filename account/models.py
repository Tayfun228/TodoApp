from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, UserManager
from django.utils.translation import ugettext_lazy as _


class CustomUser(AbstractUser):
  email = models.EmailField(_('email address'), unique=True)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name','last_name', 'username','password']

  objects=UserManager()
  def __str__(self):
      return f'{self.username}'

  


class LoginHistory(models.Model):
  user=models.ForeignKey(CustomUser,related_name='history',on_delete=models.CASCADE)
  browser=models.CharField('Browser',max_length=255,blank=True,null=True)
  os=models.CharField('Browser',max_length=255,blank=True,null=True)
  ip=models.CharField('Browser',max_length=255,blank=True,null=True)
  device=models.CharField('Browser',max_length=255,blank=True,null=True)


  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)

  