from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from account.models import WUser, License, StripeEvent
from account.forms import UserChangeForm, UserCreationForm


class LicenseAdmin(admin.ModelAdmin):
    list_display = ('purchasing_user', 'assigned_user', 'creation', 'expiration_date')
    list_filter = ('creation', )
    search_fields = ('redemption_code', 'purchasing_user.email', 'assigned_user.email')
    ordering = ('creation', 'term_in_days')


class LicenseInline(admin.TabularInline):
    model = License
    fk_name = 'purchasing_user'
    extra = 0


class WUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    inlines = [
        LicenseInline,
    ]

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_admin', 'is_active', 'created', 'account_type')
    list_filter = ('is_admin', 'is_active', 'created', 'account_type')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'account_type')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'company_name', 'address', 'city', 'state', 'zip', 'country')}),
        ('Billing Info', {'fields': ('stripe_customer_id', 'stripe_subscription_id', 'cc_type', 'cc_last_4')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'account_type', 'stripe_customer_id', 'is_admin')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email', 'created', 'account_type')
    filter_horizontal = ()

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('account_type', 'cc_type', 'cc_last_4', 'stripe_customer_id', 'stripe_subscription_id')
        return self.readonly_fields


class StripeEventAdmin(admin.ModelAdmin):
    list_display = ('stripe_event_id', 'event_type', 'created', 'user')
    list_filter = ('created', 'event_type')
    search_fields = ('stripe_event_id', 'user.email')
    ordering = ('event_type', 'created')


# Now register the new UserAdmin...
admin.site.register(WUser, WUserAdmin)
admin.site.register(License, LicenseAdmin)
admin.site.register(StripeEvent, StripeEventAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)