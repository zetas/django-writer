from django.views.generic import FormView
from django.views.generic.base import View
from django.shortcuts import render

from main.forms import ContactForm
from papers.models import PaperComment, InternalSubmission
from classes.models import Classroom
# Create your views here.


class ContactView(FormView):
    template_name = 'main/contact.html'
    form_class = ContactForm
    success_url = '/thank-you/'

    def form_valid(self, form):
        form.send_email()
        return super(ContactView, self).form_valid(form)


class DashboardView(View):
    template_name = 'main/dashboard.html'

    def get(self, request, *args, **kwargs):
        classes = request.user.classroom_set.all()

        submissions = InternalSubmission.objects.filter(classroom__in=classes)

        paper_list = []

        for s in submissions:
            paper_list.append(s.paper)

        comments_given = PaperComment.objects.filter(author=request.user)
        comments_received = PaperComment.objects.filter(paper__in=paper_list).exclude(author=request.user)

        return render(request, self.template_name, {
                                                    'classes': classes,
                                                    'comments_given': comments_given,
                                                    'comments_received': comments_received,
                                                    'submissions': submissions
                                                    })