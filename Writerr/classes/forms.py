__author__ = 'David'

from django import forms
from django.forms import ModelForm

from classes.models import Classroom


class ClassForm(forms.ModelForm):
    name = forms.CharField(max_length=200, min_length=5, widget=forms.TextInput(attrs={'placeholder': 'Name of your Class', 'class': 'form-control'}))
    students = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Insert your student\'s email addresses here. (separate multiple addresses with a comma)', 'class': 'form-control', 'rows': 10}))

    class Meta:
        model = Classroom
        fields = ['name']



class ClassFormStep2(forms.Form):
    name = forms.CharField(max_length=200, min_length=5, widget=forms.HiddenInput())
    students = forms.CharField(widget=forms.HiddenInput())

