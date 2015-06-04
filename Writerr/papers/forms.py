__author__ = 'David'

from django import forms
from django.forms import ModelForm

from papers.models import Paper, PaperSubmission, PaperComment, InternalSubmission


class PaperForm(ModelForm):
    class Meta:
        model = Paper
        fields = ['title', 'body']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title', 'id': 'title_field', 'class': 'hidden'}),
            'body': forms.Textarea(attrs={'placeholder': 'Body', 'cols': 65, 'rows': 25, 'id': 'body_field', 'class': 'hidden'})
        }


class SubmitForm(ModelForm):
    class Meta:
        model = PaperSubmission
        fields = ['submitted_to']
        widgets = {
            'submitted_to': forms.EmailInput(attrs={'placeholder': "PDF Recipient's Email", 'class': 'form-control'})
        }


class SubmitFeedback(ModelForm):
    class Meta:
        model = PaperComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': "New Feedback", 'class': 'form-control', 'rows': 4})
        }


class InternalSubmitForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(InternalSubmitForm, self).__init__(*args, **kwargs)
        self.fields['classroom'] = forms.ModelChoiceField(queryset=user.classroom_set.all())

    class Meta:
        model = InternalSubmission
        fields = ['classroom']