from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Account(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username




class Task(models.Model):
    task_name = models.CharField(max_length=1000)
    assignee = models.ForeignKey(User,on_delete=models.CASCADE)
    due_date = models.DateTimeField(auto_created=True)
    active_flag = models.BooleanField(default=True)

    def __str__(self):
        return self.task_name

class Notifications(models.Model):
    message= models.CharField(max_length=1000)
    assignee = models.ForeignKey(User,on_delete=models.CASCADE)
    task_name = models.CharField(max_length=1000,blank=True)


    def __str__(self):
        return self.assignee.username


