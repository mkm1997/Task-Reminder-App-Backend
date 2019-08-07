from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
#from django.contrib.auth.models import User
#from ReminderApp.models import Notifications

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TaskReminder.settings')
app = Celery('ReminderApp')


app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

#celery -A TaskReminder worker -l info
#celery - A TaskReminder beat - l info
#celery -A TaskReminder beat

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@app.task
def send_notifications(obj):

    message="Date have gone"

    #obj = Notifications.objects.create(message=message,assignee=obj)
    #obj.save()
    #print(obj.username)
    print("helllo")
    print("NOTIFICATION IS CALLED")

#send_notifications.apply_async(("obj",),eta=datetime.utcnow()+timedelta(seconds=5))
