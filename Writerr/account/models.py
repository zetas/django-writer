from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
import datetime as dt

from account.utils import _create_code


class WUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class WUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        db_index=True,
    )

    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    company_name = models.CharField(max_length=150, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    zip = models.PositiveIntegerField(max_length=5, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    account_type = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    cc_type = models.CharField(max_length=25, null=True, blank=True)
    cc_last_4 = models.PositiveIntegerField(max_length=4, null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255, null=True, blank=True)

    objects = WUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def blackhole(self, value):
        return True

    def get_full_name(self, no_email=False):
        # The user is identified by their email address
        if (self.first_name and self.last_name) or no_email:
            return self.first_name + ' ' + self.last_name

        return self.email
    full_name = property(get_full_name, blackhole)

    def get_billing_name(self):
        return self.get_full_name(True)

    billing_name = property(get_billing_name, blackhole)

    def get_short_name(self):
        # The user is identified by their email address
        if self.first_name:
            return self.first_name

        return self.email.split('@')[0]
    short_name = property(get_short_name, blackhole)

    def get_feedback_name(self):
        if self.first_name and self.last_name:
            return '%s %s.' % (self.first_name.capitalize(), self.last_name[:1])

        return self.email
    feedback_name = property(get_feedback_name, blackhole)

    def get_license_status(self):
        try:
            license = self.license
        except License.DoesNotExist:
            license = None

        if license is not None and isinstance(license, License):
            return True

        return False

    def get_unassigned_licenses(self):
        licenses = License.objects\
            .filter(purchasing_user__exact=self)\
            .filter(assigned_user__isnull=True)\
            .filter(sent_to__isnull=True)

        return licenses

    def get_sent_licenses(self):
        licenses = License.objects.filter(purchasing_user__exact=self).filter(sent_to__isnull=False)

        return licenses

    def get_instructor(self):
        if self.classroom:
            return self.classroom.instructor
        return False

    def has_class(self):
        if len(self.classroom_set.all()) > 0:
            return True
        return False

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class LicenseManager(models.Manager):
    def create_license(self, purchasing_user, term_in_days, *args, **kwargs):
        assigned_user = kwargs.pop('assigned_user', None)
        if assigned_user is None:
            license = self.create(purchasing_user=purchasing_user, term_in_days=term_in_days)
        else:
            license = self.create(purchasing_user=purchasing_user, term_in_days=term_in_days, assigned_user=assigned_user)

        return license

    def create_multiple_licenses(self, count, purchasing_user, term_in_days, *args, **kwargs):
        for i in range(count):
            license = self.create_license(purchasing_user, term_in_days, *args, **kwargs)
            license.save()

    def delete_user_licenses(self, purchasing_user):
        self.filter(purchasing_user=purchasing_user).delete()


class License(models.Model):
    purchasing_user = models.ForeignKey(WUser, related_name='purchased_license')
    assigned_user = models.OneToOneField(WUser, null=True, blank=True, related_name='license', primary_key=False)
    creation = models.DateTimeField(auto_now_add=True, verbose_name='license creation date')
    term_in_days = models.PositiveIntegerField(verbose_name='license term in days')
    redemption_code = models.CharField(max_length=255, unique=True, default=_create_code)
    sent_to = models.CharField(max_length=255, null=True, blank=True)

    objects = LicenseManager()

    def get_expiration_date(self):
        expiration = (self.creation + dt.timedelta(days=self.term_in_days)).date()
        return expiration.isoformat()

    def expiration_date(self):
        return self.get_expiration_date()

    def __unicode__(self):
        return self.redemption_code

    def assign(self, assigned_user):
        if assigned_user is not None and isinstance(assigned_user, WUser):
            self.assigned_user = assigned_user
            self.save()
            return True

        return False


class StripeEvent(models.Model):
    stripe_event_id = models.CharField(unique=True, max_length=150)
    created = models.DateTimeField()
    recorded = models.DateTimeField(auto_now_add=True)
    event_type = models.CharField(max_length=100)
    user = models.ForeignKey(WUser, related_name='stripe_events', null=True, blank=True)
    raw_event = models.TextField()

    def __unicode__(self):
        return self.stripe_event_id

    class Meta:
        verbose_name = 'Billing Event'
        verbose_name_plural = 'Billing Events'

        ordering = ['-recorded']