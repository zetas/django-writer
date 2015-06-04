#-------------------------------------------#
# Created By: David DV (ddv@qubitlogic.net)   
# For Project: Writerr                
# Last Modified: 2/22/14                     
# stripe_utils.py                                
#-------------------------------------------#

import datetime
import logging

from account.models import StripeEvent, WUser

logger = logging.getLogger('writerr.prodlog')


def process_stripe_event(event, *args, **kwargs):
    e = StripeEvent()
    e.stripe_event_id = event.id
    e.created = datetime.datetime.fromtimestamp(int(event.created))
    e.event_type = event.type
    e.raw_event = event

    try:
        if event.data.object.customer is not None:
            try:
                user = WUser.objects.get(stripe_customer_id=event.data.object.customer)
            except WUser.DoesNotExist:
                user = None

            if user is not None:
                e.user = user
    except Exception, ex:
        logger.error('Exception on webhook: '+ex.__str__())

    e.save()
