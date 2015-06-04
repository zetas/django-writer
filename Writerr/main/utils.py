#-------------------------------------------#
# Created By: David DV (ddv@qubitlogic.net)   
# For Project: Writerr                
# Last Modified: 2/10/14                     
# utils.py                                
#-------------------------------------------#

import json

from django.core.mail import EmailMultiAlternatives
import smtplib
from django.template.loader import get_template_from_string
from django.template.base import Context
from django.conf import settings
from django.http import HttpResponse

from main.models import EmailTemplate


def send_writerr_email(subject, to, template_name, context):

    txt_template = get_template_from_string(EmailTemplate.objects.get(name=template_name, html=False).get_body())
    html_template = get_template_from_string(EmailTemplate.objects.get(name=template_name, html=True).get_body())

    txt = txt_template.render(Context(context))
    html = html_template.render(Context(context))
    msg = EmailMultiAlternatives(subject, txt, settings.GLOBAL_EMAIL_FROM, to)
    msg.attach_alternative(html, "text/html")
    try:
        msg.send(fail_silently=False)
    except smtplib.SMTPRecipientsRefused:
        return False

    return True


class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return self.render_to_json_response(data)
        else:
            return response