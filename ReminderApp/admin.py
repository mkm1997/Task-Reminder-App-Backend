from django.contrib import admin
from .models import Task,Account,Notifications

# Register your models here.
admin.site.register(Task)
admin.site.register(Account)
admin.site.register(Notifications)


