from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.forms import User

class NotesForm(forms.ModelForm):
    class Meta:
        model=Notes
        fields=['title','description']

class DateInput(forms.DateInput):
    input_type='date'

class HomeworkForm(forms.ModelForm):
    class Meta:
        model=Homework
        widgets={'due':DateInput()}
        fields=['subject','title','description','due','is_finished']
    
class Dashboardform(forms.Form):
    text=forms.CharField(max_length=100, label="Enter Your Search ")

class Todoform(forms.ModelForm):
    class Meta:
        model=Todo
        fields=['title','is_finished']




class UserRegisterationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password1','password2']