__author__ = 'David'
from django import forms
from django.forms.fields import CharField
from django.forms import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordChangeForm
from django.utils.translation import ugettext as _

from account.models import WUser, License
from account.utils import return_country_select_list


class LicenseCodeField(CharField):
    def validate(self, value):
        # Use the parent's handling of required fields, etc.
        super(CharField, self).validate(value)

        try:
            license = License.objects.get(redemption_code=value)
        except License.DoesNotExist:
            license = None

        if license is not None:
            if license.assigned_user is not None:
                raise ValidationError(
                    _('This code has already been redeemed.'),
                    code='already_redeemed'
                )
        else:
            raise ValidationError(
                _('Invalid license code.'),
                code='invalid_license'
            )


class UserCreationForm(forms.ModelForm):
    aTypeChoices = (('personal', 'Personal'), ('enterprise', 'Enterprise'))

    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    first_name = forms.CharField(min_length=3, max_length=255, widget=forms.TextInput(
        attrs={
            'placeholder': 'First Name',
            'class': 'form-control'
        })
    )
    last_name = forms.CharField(min_length=3, max_length=255, widget=forms.TextInput(
        attrs={
            'placeholder': 'Last Name',
            'class': 'form-control'
        })
    )
    password1 = forms.CharField(min_length=6, max_length=32, widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Choose a Password',
            'class': 'form-control',
            'id': 'input-password1'
        })
    )
    password2 = forms.CharField(min_length=6, max_length=32, widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Confirm Password',
            'class': 'form-control',
            'id': 'input-password2'
        })
    )
    aType = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'aType'}))

    class Meta:
        model = WUser
        fields = ('email', 'first_name', 'last_name' )

        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Type your e-mail address', 'class': 'form-control'}),
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            if self.cleaned_data['aType'] == 'student':
                user.account_type = 'personal'
            elif self.cleaned_data['aType'] == 'instructor':
                user.account_type = 'enterprise'
            else:
                raise forms.ValidationError("Invalid Account Type")
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = WUser
        fields = ['email', 'password', 'first_name', 'last_name', 'address', 'city', 'state', 'zip', 'is_active', 'is_admin']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email Address', 'class': 'form-control'}))
    password = forms.CharField(max_length=16, min_length=6, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))


class ResetPassForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email Address', 'class': 'text'}))


class ChangePassForm(PasswordChangeForm):
    attrs = {
        'class': 'form-control'
    }

    old_password = forms.CharField(max_length=255, min_length=6, widget=forms.PasswordInput(attrs={'placeholder': 'Old Password', 'class': 'form-control'}))
    new_password1 = forms.CharField(max_length=255, min_length=6, widget=forms.PasswordInput(attrs={'placeholder': 'New Password', 'class': 'form-control'}))
    new_password2 = forms.CharField(max_length=255, min_length=6, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password', 'class': 'form-control'}))


class CheckoutForm(forms.Form):

    def set_attrs(*args, **kwargs):
        gen_attrs = {
            'class': 'form-control'
        }
        small_attrs = {
            'class': 'form-control'
        }
        med_attrs = {
            'class': 'form-control'
        }
        placeholder = kwargs.pop('placeholder', '')
        dict = {'placeholder': placeholder}
        type = kwargs.pop('type', 'general')

        if type == 'general':
            update = gen_attrs
        elif type == 'small':
            update = small_attrs
        else:
            update = med_attrs

        dict.update(update)
        return dict

    def __init__(self, *args, **kwargs):
        type = kwargs.pop('type', 'personal')
        super(CheckoutForm, self).__init__(*args, **kwargs)
        if type == 'enterprise':
             self.fields['quantity'] = forms.IntegerField(min_value=1, max_value=300, widget=forms.NumberInput(attrs=self.set_attrs(placeholder='License Quantity')))
             self.fields['company_name'] = forms.CharField(max_length=255, widget=forms.TextInput(attrs=self.set_attrs(placeholder='Company Name')))

    first_name = forms.CharField(max_length=50, min_length=3, widget=forms.TextInput(attrs=set_attrs(placeholder="First Name", type='small')))
    last_name = forms.CharField(max_length=100, min_length=3, widget=forms.TextInput(attrs=set_attrs(placeholder="Last Name", type='medium')))
    telephone = forms.CharField(max_length=15, min_length=9, widget=forms.TextInput(attrs=set_attrs(placeholder='Telephone')))
    billing_name = forms.CharField(max_length=255, min_length=6, widget=forms.TextInput(attrs=set_attrs(placeholder='Billing Name')))
    address = forms.CharField(max_length=150, min_length=5, widget=forms.TextInput(attrs=set_attrs(placeholder='Billing Address')))
    zip = forms.IntegerField(max_value=99999, min_value=10000, widget=forms.NumberInput(attrs=set_attrs(placeholder='Billing Zip', type='small')))
    city = forms.CharField(max_length=100, min_length=2, widget=forms.TextInput(attrs=set_attrs(placeholder='Billing City', type='medium')))
    state = forms.CharField(max_length=100, min_length=2, widget=forms.TextInput(attrs=set_attrs(placeholder='Billing State', type='small')))
    country = forms.ChoiceField(choices=return_country_select_list(), widget=forms.Select(attrs={'class': 'form-control'}))
    sub_type = forms.ChoiceField(choices=(('monthly', 'Monthly'), ('yearly', 'Yearly')), widget=forms.RadioSelect(attrs={'class': 'sub_type', 'id': 'sub_type_radio'}))
    stripe_token = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'stripe_token'}))
    cc_type = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'cc_type'}))
    cc_last_4 = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'last_4'}))


class RedeemLicenseCodeForm(forms.Form):
    license_code = LicenseCodeField(max_length=27, min_length=24, widget=forms.TextInput(attrs={'placeholder': 'XXXX-XXXX-XXXX-XXXX', 'class': 'form-control'}))


class SendInviteForm(forms.Form):
    recipients = forms.CharField(
        min_length=10,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Add the emails of the people to which you want to send the licenses to. Separate each email addresses by a comma.',
                'class': 'form-control',
            }
        )
    )