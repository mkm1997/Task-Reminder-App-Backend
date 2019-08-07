from .models import Task
from django import forms




class taskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['task_name',  'assignee','due_date',]



