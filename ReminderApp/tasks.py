from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from django.contrib.auth.models import User
from ReminderApp.models import Notifications
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

#celery configurations

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TaskReminder.settings')
app = Celery('ReminderApp')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)



@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))



#Notifications task
@app.task
def send_notifications(user,task_name):

    print("NOTIFICATION IS CALLED")

    #for sending the notification to the user
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notify", {"type": "user.notify",
                   "event": "Notifications",
                   "message":"The deadline has been ended for the task "+task_name,
                   "username": user})

    #creating the record of the notification
    message = "Notification has been send"
    print(message)
    obj = Notifications.objects.create(message=message,assignee=User.objects.get(username=user),task_name=task_name)
    obj.save()
    print("NOTIFICATION IS CALLED")

#send_notifications.apply_async(("obj",),eta=datetime.utcnow()+timedelta(seconds=5))

