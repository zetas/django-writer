import json
import stripe
import logging

from django.shortcuts import render, redirect, resolve_url
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import is_safe_url
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


from account.forms import UserCreationForm, LoginForm, ResetPassForm, ChangePassForm, CheckoutForm, RedeemLicenseCodeForm, SendInviteForm
from account.models import WUser, License, StripeEvent
from account.stripe_utils import process_stripe_event
from main.utils import send_writerr_email, AutoVivification
from main.forms import ContactForm

logger = logging.getLogger('writerr.logs')


class IndexView(View):
    template_name = 'account/index.html'
    new_user_template_name = 'account/index_new.html'
    form_class = ChangePassForm
    invite_form_class = SendInviteForm
    contact_form = ContactForm

    def get(self, request, *args, **kwargs):

        if not request.user.get_license_status() and request.session.get('logged_in', False) is True:
            request.session['logged_in'] = False
            return render(request, self.new_user_template_name, {'contact_form': self.contact_form()})

        activate = request.GET.get('activate', 'no')

        if activate == 'yes':
            licenses = request.user.get_unassigned_licenses()
            if bool(licenses):
                licenses[0].assign(request.user)
                return redirect('account:index')



        form = self.form_class(user=request.user)
        context = self.set_context(request.user, {'pwChangeForm': form, 'success': False})
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user, request.POST)
        success = False
        if form.is_valid():
            form.save()
            success = True

        context = self.set_context(request.user, {'pwChangeForm': form, 'success': success})

        return render(request, self.template_name, context)

    def set_context(self, user, context, *args, **kwargs):
        if user.get_license_status():
            context.update(license_expiration=user.license.get_expiration_date())
            context.update(license='Paid User')
        else:
            context.update(license_expiration=False)
            context.update(license='Free User')

        licenses = user.get_unassigned_licenses()

        sent_licenses = user.get_sent_licenses()

        context.update(attendance=user.attendance_set.all())

        if bool(licenses):
            context.update(invite_form=self.invite_form_class())
            context.update(license_count=len(licenses))

        context.update(sent_licenses=sent_licenses)

        context.update(has_unused_license=bool(licenses))

        return context


class LoginView(View):
    template_name = 'account/login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        login_success = True
        redirect_to = request.REQUEST.get('next', '')

        if form.is_valid():
            user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    if not is_safe_url(url=redirect_to, host=request.get_host()):
                        if user.account_type == 'student':
                            location = settings.LOGIN_REDIRECT_URL
                        else:
                            location = settings.LOGIN_REDIRECT_URL_INSTRUCTORS

                        redirect_to = resolve_url(location)

                    if not user.get_license_status():
                        redirect_to = resolve_url('/account/')

                    login(request, user)
                    request.session['logged_in'] = True
                    return HttpResponseRedirect(redirect_to)
                else:
                    login_success = False
            else:
                login_success = False

        return render(request, self.template_name, {'form': form, 'login_success': login_success})


def logout_view(request):
    logout(request)
    return redirect('main:index')


class SignupView(View):
    template_name = 'account/signup.html'
    form_class = UserCreationForm
    email_template_name = 'account.new_signup'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, user)
            self.send_welcome(user)
            stripe.api_key = settings.STRIPE_SECRET
            customer = stripe.Customer.create(
                email=user.email,
                metadata={
                    'account_type': user.account_type
                }
            )
            user.stripe_customer_id = customer.id
            user.save()

            request.session['logged_in'] = True
            return redirect('account:index')

        return render(request, self.template_name, {'form': form})

    def send_welcome(self, user):
        short_name = user.get_short_name()
        subject = "Hi "+short_name+"! Welcome to Writerr"
        recipient = [user.email, ]

        data = {'shortName': short_name}
        send_writerr_email(subject, recipient, self.email_template_name, data)


class ResetPassView(View):
    form_class = ResetPassForm
    email_template_name = 'account.pass_reset'

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def get(self, request, *args, **kwargs):
        return redirect('main:index')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            reset_email = form.cleaned_data['email']
            try:
                user = WUser.objects.get(email=reset_email)
            except WUser.DoesNotExist:
                user = None
            if user is not None:
                new_pass = WUser.objects.make_random_password(8)
                user.set_password(new_pass)
                user.save()

                self.send_new_pass(user, new_pass)

                data = {'found': 'True', }
            else:
                data = {'found': 'False', }
        else:
            data = {'found': 'Invalid', 'errors': form.errors, }

        return self.render_to_json_response(data)

    def send_new_pass(self, user, new_pass):
        short_name = user.get_short_name()
        subject = "Password Reset Request on Writerr"
        recipient = [user.email, ]

        data = {'shortName': short_name, 'newPass': new_pass}
        send_writerr_email(subject, recipient, self.email_template_name, data)


# TODO: Lock this down to allow host-only access.
class LicenseVerifyView(View):

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = {
                'license_status': request.user.get_license_status(),
                'account_type': request.user.account_type,
            }
            return self.render_to_json_response(data)


class UpgradeView(View):
    template = 'account/upgrade.html'
    form_class = RedeemLicenseCodeForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template, {'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            if not request.user.get_license_status():
                license = License.objects.get(redemption_code=form.cleaned_data['license_code'])

                """
                It ensures user doesn't already have an associated license
                """
                license.assigned_user = request.user
                license.save()

            return redirect('account:index')

        return render(request, self.template, {'form': form, })


class CheckoutView(View):
    form_class = CheckoutForm
    template = 'account/checkout.html'
    email_template_name = 'account.checkout_success'

    def create_sub(self, user, customer, plan, quantity):
        subscription = customer.subscriptions.create(plan=plan, quantity=quantity)
        user.stripe_subscription_id = subscription.id
        user.save()

    def get(self, request, *args, **kwargs):
        data = {
            'sub_type': 'monthly',
        }
        user = request.user

        for field in self.form_class(type=user.account_type).fields:
            if hasattr(user, field) and getattr(user, field) is not None:
                    data.update({field: getattr(user, field).__str__()})

        return render(request, self.template, {'form': self.form_class(type=user.account_type, initial=data), 'stripe_key': settings.STRIPE_PUBLISHABLE})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, type=request.user.account_type)
        if form.is_valid():
            user = request.user
            stripe.api_key = settings.STRIPE_SECRET
            token = form.cleaned_data['stripe_token']
            quantity = form.cleaned_data.get('quantity', 1)
            try:
                customer = stripe.Customer.retrieve(user.stripe_customer_id)
            except stripe.InvalidRequestError, e:
                if e.__str__() == "No such customer: " + user.stripe_customer_id:
                    logger.exception('Invalid request on stripe customer retrieve but unable to catch it!')
                    customer = stripe.Customer.create(
                        email=user.email,
                        metadata={
                            'account_type': user.account_type
                        }
                    )
                    user.stripe_subscription_id = None
                    user.stripe_customer_id = customer.id
                    user.save()
                #else:
                #    logger.exception('Invalid request on stripe customer retrieve but unable to catch it!')

            customer.card = token
            customer.save()

            if form.cleaned_data['sub_type'] == 'yearly':
                license_range = 365
                price = settings.STRIPE_YEARLY_COST
                period = 'year'
            else:
                license_range = 30
                price = settings.STRIPE_MONTHLY_COST
                period = 'month'

            context = {
                'shortName': user.get_short_name(),
                'period': period,
                'last_4': form.cleaned_data['cc_last_4'],
                'license_cost': price,
            }

            if user.stripe_subscription_id is None:
                self.create_sub(user, customer, form.cleaned_data['sub_type'], quantity)
                if user.account_type == 'personal':
                    license = License.objects.create_license(user, license_range, user)
                    license.save()

                    context.update({'license_count': 1, 'total_cost': price*1, 'next_charge_date': license.get_expiration_date()})

                else:
                    License.objects.create_multiple_licenses(quantity, user, license_range)
                    license = user.get_unassigned_licenses()[0]
                    context.update({'license_count': quantity, 'total_cost': price*quantity, 'next_charge_date': license.get_expiration_date()})

            else:
                subscription = customer.subscriptions.retrieve(user.stripe_subscription_id)

                original_plan = subscription.plan.id
                selected_plan = form.cleaned_data['sub_type']

                if original_plan == selected_plan:
                    original_quantity = subscription.quantity
                    subscription.quantity = original_quantity + quantity
                    subscription.save()
                    License.objects.create_multiple_licenses(quantity, user, license_range)
                    license = user.get_unassigned_licenses()[0]
                    context.update({'license_count': quantity, 'total_cost': price*quantity, 'next_charge_date': license.get_expiration_date()})
                else:
                    License.objects.delete_user_licenses(user)
                    subscription.delete()
                    self.create_sub(user, customer, form.cleaned_data['sub_type'], quantity)
                    License.objects.create_multiple_licenses(quantity, user, license_range)
                    license = user.get_unassigned_licenses()[0]
                    context.update({'license_count': quantity, 'total_cost': price*quantity, 'next_charge_date': license.get_expiration_date()})

            # Update User Data
            for key in form.cleaned_data.keys():
                if hasattr(user, key):
                    setattr(user, key, form.cleaned_data[key])

            user.save()

            send_writerr_email('Thank you for your order.', [user.email, ], self.email_template_name, context)

            return redirect('account:checkout_success')

        return render(request, self.template, {'form': form, 'stripe_key': settings.STRIPE_PUBLISHABLE})


class CheckoutSuccessView(View):
    template_name = 'account/checkout_success.html'
    contact_form = ContactForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'contact_form': self.contact_form()})


class InviteView(View):
    form_class = SendInviteForm
    email_template_name_new_user = 'account.assigned_new'
    email_template_name = 'account.assigned'

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def get(self, request, *args, **kwargs):
        return redirect('account:index')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        data = AutoVivification()
        if form.is_valid():
            emails = form.cleaned_data['recipients']
            licenses = request.user.get_unassigned_licenses()

            #Double check the user has licenses available, just in case.
            if bool(licenses):
                license_count = len(licenses)

                #Only split the amount of licenses they have available.
                email_list = emails.split(',', license_count)
                license_list = list(licenses)

                for email in email_list:
                    e = email.strip()

                    import re
                    if not re.match(r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", e):
                        data[e]['error'] = "invalid_email"
                    else:

                        try:
                            user = WUser.objects.get(email=e)
                        except WUser.DoesNotExist:
                            user = None

                        if user is not None:
                            data[e]['exists'] = True
                            if user.get_license_status():
                                data[e]['already_licensed'] = True
                            else:
                                license = license_list.pop(0)
                                result = license.assign(user)

                                context = {
                                    'shortName': user.get_short_name(),
                                    'purchaser': license.purchasing_user.get_full_name()
                                }

                                send_writerr_email('New License Assigned', [user.email, ], self.email_template_name, context)

                                data[e]['already_licensed'] = False
                                data[e]['result'] = result
                        else:
                            try:
                                sent_lic = License.objects.get(sent_to=e)
                            except License.DoesNotExist:
                                sent_lic = None

                            if sent_lic is not None:
                                data[e]['already_sent'] = True
                                license = sent_lic
                            else:
                                data[e]['already_sent'] = False
                                license = license_list.pop(0)
                                license.sent_to = e
                                license.save()

                            data[e]['exists'] = False
                            data[e]['already_licensed'] = False

                            context = {
                                'shortName': e.split('@')[0],
                                'purchaser': license.purchasing_user.get_full_name(),
                                'code': license.redemption_code
                            }

                            subject = license.purchasing_user.get_short_name()+' has bought you a license!'

                            send_writerr_email(subject, [e, ], self.email_template_name_new_user, context)
            else:
                data['error'] = 'no_licenses_available'
        else:
            data['error'] = 'invalid_form'
            data['response'] = form.errors

        return self.render_to_json_response(data)


class RedeemView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse("<html></html>")



@csrf_exempt
def webhook_view(request):
    event_json = json.loads(request.body)

    stripe.api_key = settings.STRIPE_SECRET

    try:
        stripe_event = stripe.Event.retrieve(event_json['id'])
    except stripe.InvalidRequestError:
        stripe_event = None

    if stripe_event is not None:
        try:
            existing_event = StripeEvent.objects.get(stripe_event_id=stripe_event.id)
        except StripeEvent.DoesNotExist:
            existing_event = None

        if existing_event is None:
            process_stripe_event(stripe_event)

    return HttpResponse('<html>OK</html>')



