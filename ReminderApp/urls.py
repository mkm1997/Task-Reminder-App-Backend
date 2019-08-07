from django.contrib import admin
from django.urls import path,re_path,include
from . import views

urlpatterns = [
    # path("project/<int:project_id>",views.project),
    re_path(r'^notify/$',views.notify,name='notify'),
    re_path(r'^task/$',views.createTask,name='taskform'),
    re_path(r'^updatetask/$',views.updateTask,name='update'),
    re_path(r'^viewTask/$',views.viewTask,name='viewTask'),
    re_path(r'^select/$',views.selectTask,name='select'),
    re_path(r'^getalltask/$',views.getAllTask.as_view(),name='getalltask'),
    re_path(r'^getalluser/$',views.getAllUser.as_view(),name='getalluser'),
    re_path(r'^login/$',views.loginUser,name='login'),
    re_path(r'^signup/$',views.signup,name="signup"),
    re_path(r'^logout/$', views.logout, name="logout"),
    re_path(r'^getallnotification/$', views.getAllNotification.as_view(), name='notification')

]