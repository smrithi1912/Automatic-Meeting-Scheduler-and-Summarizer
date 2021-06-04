from .models import employee
from django import forms
from django.contrib.admin.widgets import AdminDateWidget,AdminTimeWidget, AdminSplitDateTime  
# import GeeksModel from models.py
from .models import meeting
  
# create a ModelForm
class Scheduler(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = meeting
        fields = 'title','date','start_time','end_time','participants','link'
        widgets ={
            'start_time' : AdminTimeWidget(),
            'end_time' : AdminTimeWidget(),
            'date' : AdminDateWidget(),
        }
