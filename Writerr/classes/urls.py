__author__ = 'David'

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from django.views.decorators.cache import never_cache

from classes.views import ClassCreate, ClassList, ClassUpdate, ClassDelete, ClassView

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(pattern_name='classes:create'), name='index'),
    url(r'^add/$', login_required(ClassCreate.as_view()), name='create'),
    url(r'^add/(?P<step>\d+)$', login_required(ClassCreate.as_view()), name='create_step'),
    url(r'^(?P<pk>\d+)/$', login_required(ClassUpdate.as_view()), name='update'),
    url(r'^view/(?P<code>\w+)/$', login_required(ClassView.as_view()), name='detail'),
    url(r'^(?P<pk>\d+)/delete/$', login_required(ClassDelete.as_view()), name='delete'),
    url(r'^list/$', never_cache(login_required(ClassList.as_view())), name='list'),
)