from django.db import models
from account.models import CustomUser

# Create your models here.
STATUS_CHOICES = (
    (1, "View"),
    (2, "View and write comment"),
)

class Task(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='User', related_name='task' ,on_delete=models.CASCADE)
    title = models.CharField('Title', max_length=255)
    description = models.TextField('Description', max_length=5000, null=True, blank=True)
    remind_me=models.BooleanField(default=True)
    is_completed=models.BooleanField(default=False)
    expired_at=models.DateTimeField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    text=models.CharField('Comment',max_length=255, blank=False, null=False)
    user=models.ForeignKey(CustomUser,related_name='comments',on_delete=models.CASCADE)
    task=models.ForeignKey(Task,related_name='comments',on_delete=models.CASCADE)

class Share(models.Model):
    task=models.ForeignKey(Task,related_name='share',on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUser,related_name='share',on_delete=models.CASCADE)
    status=models.IntegerField(choices=STATUS_CHOICES, default=1)  
