from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from account import views
from account.views import SignupView, \
    LoginView, \
    ResetPassView, \
    IndexView, \
    LicenseVerifyView, \
    CheckoutView, \
    UpgradeView, \
    InviteView, \
    RedeemView, \
    CheckoutSuccessView

urlpatterns = patterns('',
    url(r'^$', login_required(IndexView.as_view()), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^reset/$', ResetPassView.as_view(), name='reset_pass'),
    url(r'^verify/$', login_required(LicenseVerifyView.as_view()), name='verify'),
    url(r'^upgrade/$', login_required(UpgradeView.as_view()), name='upgrade'),
    url(r'^checkout/success/$', login_required(CheckoutSuccessView.as_view()), name='checkout_success'),
    url(r'^checkout/$', login_required(CheckoutView.as_view()), name='checkout'),
    url(r'^send_invite/$', login_required(InviteView.as_view()), name='send_invites'),
    url(r'^redeem/(?P<code>\w+)$', login_required(RedeemView.as_view()), name='redeem_invite'),
    url(r'^webhooks/$', views.webhook_view, name='unused_webhooks'),

)