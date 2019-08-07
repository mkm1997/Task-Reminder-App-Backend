from collections import OrderedDict

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import TaskSerializers, userSrializers, NotificationsSerializers
from .models import Task, Notifications
import json
from .tasks import send_notifications
from .forms import taskForm
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from dateutil import tz
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.


import datetime


#function to adding status in the list
def get_error_response(get_response):
    response = OrderedDict([("status", "error")])
    response_message = OrderedDict([("message", "Not found")])
    response.update(response_message)
    get_response.data = response
    return get_response


#for login of the user
@csrf_exempt
@api_view(["GET","POST"])
def loginUser(request):

    if request.method == 'POST':
        try:
            request_json = json.loads(request.body.decode("utf-8"))  # when postman
        except Exception as E:
            request_json = request.POST.copy()


        print(request_json)
        try:
            username = request_json['username']
            password = request_json['password']
        except Exception as e:
            data = {'status': 'failure',
                    'message': str(e)}
            return HttpResponse(json.dumps(data), content_type='text/javascript')
        try:
            user = authenticate(username = username, password=password)  # authenticate that user is exist or not
            if user:
                if user.is_active:
                    login(request, user)
                    token, _ = Token.objects.get_or_create(user=user)

                    data = {'status': 'success',
                            'token':token.key,
                            'message': 'Login Successfully'}
                    print(data)
                    return HttpResponse(json.dumps(data), content_type='text/javascript')
                else:
                    data = {'status': 'failure',
                            'message': 'user is not active'}

                    return HttpResponse(json.dumps(data), content_type='text/javascript')
            else:
                print("user is not axist")
                data = {'status': 'failure',
                        'message': 'user does not exists'}

                return HttpResponse(json.dumps(data), content_type='text/javascript')
        except Exception as d:
            data = {'status': 'failure',
                    'message': str(d)}

            return HttpResponse(json.dumps(data), content_type='text/javascript')


    data = {'status': 'failure',
             'message': 'Get Request is not allowed'}

    return HttpResponse(json.dumps(data), content_type='text/javascript')




@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            request_json = json.loads(request.body.decode("utf-8"))  # when postman
        except Exception as E:
            request_json = request.POST.copy()
        print(request_json)
        try:
            obj = User.objects.create_user(username= request_json["username"],password=request_json["password"])
            obj.save()
            data = {'status': 'success',
                    'message': 'User Created Successfully'}
            return HttpResponse(json.dumps(data), content_type='text/javascript')
        except Exception as e:
            data = {'status': 'failure',
                    'message': str(e)}
            return HttpResponse(json.dumps(data), content_type='text/javascript')
    data = {'status': 'failure',
                    'message': "GET request is not allowed"}
    return HttpResponse(json.dumps(data), content_type='text/javascript')


@csrf_exempt
@api_view(["GET","POST"])
def Logout(request):
    if request.method == "GET":
        if not request.user.is_anonymous:
            logout(request)
            data = {'status': 'success',
                    'message': 'Logout successfully'}
            return HttpResponse(json.dumps(data), content_type='text/javascript')
        else:
            data = {'status': 'success',
                    'message': 'User is already logout'}
            return HttpResponse(json.dumps(data), content_type='text/javascript')
    data = {'status':'failure',
            'message':'Post request is not allowed'}
    return HttpResponse(json.dumps(data),content_type='text/javascript')



@csrf_exempt
@api_view(["POST","GET"])
def createTask(request):
    if request.method == 'POST':
        try:
            request_json = json.loads(request.body.decode("utf-8"))  # when postman
        except Exception as E:
            request_json = request.POST.copy()
        try:
            if request.user.is_authenticated:
                print(request_json)

                date_str = request_json["due_date"]
               # datetime_object = datetime.strptime('06/05/2019  1:33PM', '%m/%d/%Y %I:%M%p')

                format_str = '%d/%m/%Y, %H:%M:%S' # The format
                datetime_obj = datetime.datetime.strptime(date_str, format_str)
                print(datetime_obj.date())
                request_json["due_date"] = datetime_obj.date()
                from_zone = tz.tzutc()
                to_zone = tz.tzlocal()
                utc = datetime_obj.replace(tzinfo=to_zone)
                central = utc.astimezone(from_zone)

                obj =Task.objects.create(assignee =  User.objects.get(username= request_json["assignee"]),
                                         due_date= central,task_name= request_json["task_name"])
                obj.save()
                ####sending the notifications Task to the celery with parameter user

                send_notifications.apply_async((request_json["assignee"],request_json['task_name']), eta=central)

                data = {
                    "status":"success",
                    "message":"Task Created Succuessfully"
                }
                return HttpResponse(json.dumps(data),content_type='text/javascript')
            else:
                data = {
                    "status": "failure",
                    "message": "You have not permission to add Task"
                }
                return HttpResponse(json.dumps(data), content_type='text/javascript')

        except Exception as e:
            data = {'status': 'failure',
                    'message': str(e)}

            return HttpResponse(json.dumps(data), content_type='text/javascript')


    	data = {
                    "status": "failure",
                    "message": "You have not permission to add Task"
                }
        return HttpResponse(json.dumps(data), content_type='text/javascript')




@api_view(["POST","GET"])
@csrf_exempt
def updateTask(request):
    if request.method == 'POST':
        try:
            request_json = json.loads(request.body.decode("utf-8"))  # when postman
        except Exception as E:
            request_json = request.POST.copy()
        try:
            if request.user.is_authenticated:
                date_str = request_json["due_date"]
                # datetime_object = datetime.strptime('06/05/2019  1:33PM', '%m/%d/%Y %I:%M%p')

                format_str = '%d/%m/%Y, %H:%M:%S'  # The format
                datetime_obj = datetime.datetime.strptime(date_str, format_str)
                print(datetime_obj.date())
                request_json["due_date"] = datetime_obj.date()
                from_zone = tz.tzutc()
                to_zone = tz.tzlocal()
                utc = datetime_obj.replace(tzinfo=to_zone)
                central = utc.astimezone(from_zone)
                print("Id is ",request_json['id'])
                obj=Task.objects.filter(task_name = request_json["old_task_name"],assignee = request.user )[0];
                obj.task_name = request_json['task_name']
                obj.due_date = central
                obj.save()

                send_notifications.apply_async((request_json["assignee"], request_json['task_name']), eta=central)

                data = {
                    "status":"success",
                    "message":"Task Updated Succuessfully"
                }
                return HttpResponse(json.dumps(data),content_type='text/javascript')
            else:
                data = {
                    "status": "failure",
                    "message": "You have not permission to update Task"
                }
                return HttpResponse(json.dumps(data), content_type='text/javascript')

        except Exception as e:
            data = {'status': 'failure',
                    'message': str(e)}

            return HttpResponse(json.dumps(data), content_type='text/javascript')



from rest_framework import filters

class getAllTask(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializers
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('assignee__username',)



    def get(self, request, *args, **kwargs):
        get_response = super().get(request, *args, **kwargs)
        if not get_response.data:
            return get_error_response(get_response)
        response = OrderedDict([("status", "success")])
        adv_data = OrderedDict([("data", get_response.data)])
        response.update(adv_data)
        get_response.data = response
        return get_response






class getAllNotification(generics.ListAPIView):
    # permission_classes = ((AllowAny,))
    serializer_class = NotificationsSerializers

    def get(self, request, *args, **kwargs):
        get_response = super().get(request, *args, **kwargs)
        if not get_response.data:
            return get_error_response(get_response)
        response = OrderedDict([("status", "success")])
        adv_data = OrderedDict([("data", get_response.data)])
        response.update(adv_data)
        get_response.data = response
        return get_response

    def get_queryset(self):
        query = self.request.query_params.dict()
        queryset = Notifications.objects.filter(assignee = self.request.user)
        return queryset



class getAllUser(generics.ListAPIView):
    # permission_classes = ((AllowAny,))
    serializer_class = userSrializers

    def get(self, request, *args, **kwargs):
        get_response = super().get(request, *args, **kwargs)
        if not get_response.data:
            return get_error_response(get_response)
        response = OrderedDict([("status", "success")])
        adv_data = OrderedDict([("data", get_response.data)])
        response.update(adv_data)
        get_response.data = response
        return get_response

    def get_queryset(self):
        queryset = User.objects.filter(is_active=True)
        return queryset


