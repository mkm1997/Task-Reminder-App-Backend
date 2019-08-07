from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task,Notifications

class userSrializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email')

class TaskSerializers(serializers.ModelSerializer):
    assignee = userSrializers()
    class Meta:
        model = Task
        fields ='__all__'

class NotificationsSerializers(serializers.ModelSerializer):
    assignee = userSrializers()
    class Meta:
        model = Notifications
        fields ='__all__'
