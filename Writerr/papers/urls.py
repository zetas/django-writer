from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from django.views.decorators.cache import never_cache

from papers.views import PaperCreate, \
    PaperUpdate, \
    PaperDelete, \
    PaperList, \
    PaperSubmit, \
    PaperSubmissionList, \
    FeedbackSubmit, \
    PermalinkView, \
    PaperInternalSubmit

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(pattern_name='papers:create'), name='index'),
    url(r'^add/$', never_cache(login_required(PaperCreate.as_view())), name='create'),
    url(r'^(?P<pk>\d+)/$', never_cache(login_required(PaperUpdate.as_view())), name='update'),
    url(r'^instructor/(?P<pk>\d+)/$', never_cache(login_required(PaperUpdate.as_view())), name='instructor'),
    url(r'^(?P<pk>\d+)/delete/$', never_cache(login_required(PaperDelete.as_view())), name='delete'),
    url(r'^list/$', never_cache(login_required(PaperList.as_view())), name='list'),
    url(r'^submit/list/$', never_cache(login_required(PaperSubmissionList.as_view())), name='submit_list'),
    url(r'^(?P<pk>\d+)/submit/$', never_cache(login_required(PaperSubmit.as_view())), name='submit'),
    url(r'^(?P<pk>\d+)/internal_submit/$', never_cache(login_required(PaperInternalSubmit.as_view())), name='internal_submit'),
    url(r'^(?P<pk>\d+)/feedback/$', never_cache(login_required(FeedbackSubmit.as_view())), name='feedback'),
    url(r'^instructor/(?P<pk>\d+)/feedback/$', never_cache(login_required(FeedbackSubmit.as_view())), name='instructor_feedback'),
    url(r'^public/(?P<code>\w+)', PermalinkView.as_view(), name='permalink'),
)