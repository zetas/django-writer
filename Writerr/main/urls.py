from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from main.views import ContactView, DashboardView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='main/index.html'), name='index'),
    url(r'^students/$', TemplateView.as_view(template_name='main/students.html') , name='students'),
    url(r'^instructors/$', TemplateView.as_view(template_name='main/instructors.html') , name='instructors'),
    url(r'^pricing/$', TemplateView.as_view(template_name='main/pricing.html') , name='pricing'),
    url(r'^contact/$', ContactView.as_view(), name='contact'),
    url(r'^thank-you/$', TemplateView.as_view(template_name='main/contact_thankyou.html'), name='contact_thanks'),
    url(r'^dashboard/$', login_required(DashboardView.as_view()), name='dashboard'),
)