__author__ = 'David'

from django import forms
from django.conf import settings
from main.utils import send_writerr_email


class ContactForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Full Name', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'E-mail address', 'class': 'form-control'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Phone number', 'class': 'form-control'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'What is your inquiry about?', 'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Let us know how we can help', 'rows': 8, 'class': 'form-control'}))

    def send_email(self):

        send_writerr_email(
            settings.CONTACT_EMAIL_SUBJECT,
            [settings.CONTACT_EMAIL_TO, ],
            settings.CONTACT_EMAIL_TEMPLATE,
            self.cleaned_data
        )