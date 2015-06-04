from django.conf.urls import patterns, include, url

from django.contrib import admin
from .sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^papers/', include('papers.urls', namespace='papers')),
    url(r'^classes/', include('classes.urls', namespace='classes')),
    url(r'^account/', include('account.urls', namespace='account')),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'', include('main.urls', namespace='main')),
)
