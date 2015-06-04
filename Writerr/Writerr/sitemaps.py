"""
Created By: David DV (ddv@qubitlogic.net)
For Project: Writerr
Last Modified: 2/26/14
sitemaps.py
"""

from django.contrib import sitemaps
from django.core.urlresolvers import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['main:index', 'main:students', 'main:instructors', 'main:pricing', 'main:login', 'main:signup', 'main:contact']

    def location(self, item):
        return reverse(item)