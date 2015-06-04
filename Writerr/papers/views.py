import json
import ho.pisa as pisa
import time
import logging

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import View
from django.views.generic import ListView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.text import slugify
from django.conf import settings
from django.template.loader import get_template
from django.template import Context
from django.utils.html import strip_tags
from django.contrib.sites.models import Site

from papers.forms import PaperForm, SubmitForm, SubmitFeedback, InternalSubmitForm
from papers.models import Paper, PaperSubmission, PaperComment, Permalink, InternalSubmission
from main.utils import send_writerr_email, AjaxableResponseMixin

logger = logging.getLogger('writerr.logs')


class PaperCreate(AjaxableResponseMixin, CreateView):
    model = Paper
    fields = ['title', 'body']
    form_class = PaperForm
    submit_form_class = SubmitForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.title = strip_tags(form.instance.title)
        return super(PaperCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PaperCreate, self).get_context_data(**kwargs)
        request = self.kwargs.get('request', None)

        if request is not None:
            context['submit_form'] = self.submit_form_class(request.POST)
        else:
            context['submit_form'] = self.submit_form_class()

        return context


class PaperUpdate(AjaxableResponseMixin, UpdateView):
    model = Paper
    fields = ['title', 'body']
    form_class = PaperForm
    submit_form_class = SubmitForm
    feedback_form_class = SubmitFeedback
    internal_submit_form = InternalSubmitForm

    def get_context_data(self, **kwargs):
        context = super(PaperUpdate, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs.get('pk')
        urlname = self.request.resolver_match.url_name
        request = self.kwargs.get('request', None)
        current_site = Site.objects.get_current()

        if request is not None:
            context['submit_form'] = self.submit_form_class(request.POST)
        else:
            context['submit_form'] = self.submit_form_class()

        context['feedback'] = PaperComment.objects.filter(paper=self.object)
        context['feedback_form'] = self.feedback_form_class()
        context['permalink'] = self.object.generate_permalink()
        context['url'] = current_site.domain
        context['http'] = settings.HTTP
        context['urlname'] = urlname
        context['internal_submit_form'] = self.internal_submit_form(user=self.request.user)

        return context

    def get_queryset(self):
        urlname = self.request.resolver_match.url_name

        if urlname == 'instructor':
            classes = self.request.user.classroom_set.all()

            submissions = InternalSubmission.objects.filter(classroom__in=classes)

            paper_list = []

            for s in submissions:
                paper_list.append(s.paper.id)

            return Paper.objects.filter(pk__in=paper_list)

        return Paper.objects.filter(user=self.request.user)

    def form_valid(self, form):
        urlname = self.request.resolver_match.url_name

        if urlname == 'instructor':
            return redirect('account:index')

        form.instance.title = strip_tags(form.instance.title)
        return super(PaperUpdate, self).form_valid(form)


class PaperDelete(DeleteView):
    model = Paper
    success_url = reverse_lazy('papers:create')

    def get_queryset(self):
        return Paper.objects.filter(user=self.request.user)

    def dispatch(self, *args, **kwargs):
        # maybe do some checks here for permissions ...

        resp = super(PaperDelete, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            return resp


class PaperList(ListView):
    context_object_name = 'paper_list'

    def get_queryset(self):
        return Paper.objects.filter(user=self.request.user)


class PaperSubmissionList(ListView):
    context_object_name = 'submission_list'

    def get_queryset(self):
        return PaperSubmission.objects.filter(paper__user__exact=self.request.user)


class PaperSubmit(View):
    pdf_template = 'papers/pdf.html'
    email_template_name = 'papers.submission'
    form_class = SubmitForm

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def get_paper_html(self, paper):
        template = get_template(self.pdf_template)

        context = {
            'logo': settings.STATIC_ROOT + '/main/images/logo.png',
            'title': paper.title,
            'author': paper.user.get_full_name(),
            'body': paper.body
        }

        html = template.render(Context(context))

        return html

    def send_pdf(self, request, submission):
        link_href = submission.link_href()
        link = '<a href="' + link_href + '" target="_blank">' + submission.slug + '.pdf</a>'
        sender = request.user.get_short_name()
        shortName = submission.submitted_to.split('@')[0]

        context = {
            'link_href': link_href,
            'link': link,
            'sender': sender,
            'shortName': shortName
        }

        send_writerr_email(sender + ' sent you a paper.', [submission.submitted_to, ], self.email_template_name, context)

    def get(self, request, *args, **kwargs):
        return redirect('papers:create')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                paper = Paper.objects.get(pk=kwargs.get('pk'), user=self.request.user)
            except Paper.DoesNotExist:
                paper = None

            if paper is not None:
                submission = PaperSubmission()

                if len(paper.title) >= 25:
                    title = paper.title[0:25]
                else:
                    title = paper.title

                raw_file_name = request.user.get_short_name() + ' ' + paper.id.__str__() + ' ' + title + ' ' + time.time().__int__().__str__()

                file_name = slugify(raw_file_name) + '.pdf'

                submission.slug = slugify(raw_file_name)
                submission.paper = paper
                submission.submitted_to = form.cleaned_data['submitted_to']

                output_file = open(settings.PDF_SAVE_LOCATION + file_name, 'w+b')
                pisaStatus = pisa.CreatePDF(self.get_paper_html(paper), dest=output_file)

                output_file.close()
                if pisaStatus.err == 0:
                    data = {'result': True}
                else:
                    data = {'result': False, 'error': 'bad_pdf'}

                submission.save()

                self.send_pdf(request, submission)
            else:
                data = {'result': False, 'error': 'no_paper'}
        else:
            data = {'result': False, 'error': form.errors}

        return self.render_to_json_response(data)


class PaperInternalSubmit(AjaxableResponseMixin, CreateView):
    model = InternalSubmission
    fields = ['classroom']
    form_class = InternalSubmitForm

    def get_form_kwargs(self):
        kwargs = super(PaperInternalSubmit, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        paper_pk = self.kwargs.pop('pk')

        try:
            paper = Paper.objects.get(pk=paper_pk, user=self.request.user)
        except Paper.DoesNotExist:
            paper = None

        if paper:
            form.instance.paper = paper
            return super(PaperInternalSubmit, self).form_valid(form)


class FeedbackSubmit(AjaxableResponseMixin, CreateView):
    model = PaperComment
    fields = ['content']
    form_class = SubmitFeedback

    def get_context_data(self, **kwargs):
        context = super(FeedbackSubmit, self).get_context_data(**kwargs)
        context['urlname'] = self.request.resolver_match.url_name
        return context

    def form_valid(self, form):
        paper_pk = self.kwargs.pop('pk')
        urlname = self.request.resolver_match.url_name
        paper = None
        if urlname == 'instructor_feedback':
            classes = self.request.user.classroom_set.all()

            submissions = InternalSubmission.objects.filter(classroom__in=classes)

            for s in submissions:
                if s.paper.id == int(paper_pk):
                    paper = s.paper
                    break
        else:
            try:
                paper = Paper.objects.get(pk=paper_pk, user=self.request.user)
            except Paper.DoesNotExist:
                paper = None

        if paper is not None:
            form.instance.paper = paper
            form.instance.author = self.request.user
            return super(FeedbackSubmit, self).form_valid(form)


class PermalinkView(View):
    template_name = 'papers/permalink.html'

    def get(self, request, *args, **kwargs):
        code = kwargs.get('code', None)
        if code is not None:
            try:
                link = Permalink.objects.get(code=code)
            except Permalink.DoesNotExist:
                link = None

            if link is not None:
                return render(request, self.template_name, {'paper': link.paper})

        return redirect('main:index')


#def upload_image_view(request):
#    if request.POST:
