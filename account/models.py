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


