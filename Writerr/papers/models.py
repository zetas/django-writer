from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.conf import settings

from account.models import WUser
from classes.models import Classroom
from papers.utils import _create_permalink_code


class Paper(models.Model):
    user = models.ForeignKey(WUser)
    title = models.CharField(max_length=255)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
            ("analyze_papers", "Can analyze their own papers."),
        )
        ordering = ['-date_modified']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('papers:update', kwargs={'pk': self.pk})

    def generate_permalink(self):
        try:
            link = Permalink.objects.get(paper=self)
        except Permalink.DoesNotExist:
            link = None

        if link is None:
            link = Permalink.objects.create(paper=self)

        return link


class PaperSubmission(models.Model):
    paper = models.ForeignKey(Paper)
    slug = models.CharField(max_length=350)
    submitted_to = models.EmailField()
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.slug

    def user(self):
        return self.paper.user

    def link_href(self):
        current_site = Site.objects.get_current()
        url = current_site.domain
        href = settings.HTTP + url + settings.PDF_URL_BASE + self.slug + '.pdf'

        return href

    class Meta:
        verbose_name = 'Submission'
        verbose_name_plural = 'Submissions'

        ordering = ['-date_submitted']


#Unused
class AnalyzationResult(models.Model):
    paper = models.ForeignKey(Paper)
    result = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


class PaperComment(models.Model):
    paper = models.ForeignKey(Paper)
    author = models.ForeignKey(WUser)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')

    def __unicode__(self):
        return "%s commented on %s" % (self.author, self.paper)

    def get_absolute_url(self):
        return reverse('papers:update', kwargs={'pk': self.paper.pk})

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedback Comments'

        ordering = ['created']


class Permalink(models.Model):
    paper = models.ForeignKey(Paper)
    code = models.CharField(max_length=255, unique=True, default=_create_permalink_code)
    created = models.DateTimeField(auto_now_add=True)


class InternalSubmission(models.Model):
    paper = models.ForeignKey(Paper)
    classroom = models.ForeignKey(Classroom)
    date_submitted = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('papers:update', kwargs={'pk': self.paper.pk})

