from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm, SetPasswordForm)
from .models import UserBase, Address
import re
from phonenumber_field.formfields import PhoneNumberField
import pathlib

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}
    ))

    error_messages = {
        'invalid_login': "Please enter a correct email address and password. Note that both fields are case-sensitive.",
        'inactive': "This account is inactive.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Email address'})


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(min_length=4, max_length=50, help_text='Required',
                               widget=forms.TextInput(attrs={'placeholder': 'Enter username'}))
    email = forms.EmailField(max_length=150, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Please enter password'}),
                               min_length=5, max_length=50)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Please enter password again'}),
                                min_length=5, max_length=50)

    class Meta:
        model = UserBase
        fields = ('username', 'email')

    def clean_user_name(self):
        username = self.cleaned_data['username'].lower()
        filter_user = UserBase.objects.filter(username=username).exists()

        filter_re = r"^(?=.{3,20}$)(?![_.-])(?!.*[_.]{2})[a-zA-Z0-9._-]+(?<![_.])$"

        if filter_user:
            raise forms.ValidationError("Username already exists")
        elif not re.search(filter_re, username):
            raise forms.ValidationError('You can only use letters, numbers and dot in the username')

        return username

    def clean_password2(self):
        clean_data = self.cleaned_data

        password = clean_data['password']
        password2 = clean_data['password2']

        if len(password) < 5:
            raise forms.ValidationError('Your password must be at least 5 characters')
        if not any(char.isalpha() for char in password):
            raise forms.ValidationError('Your password must use at least 1 letter')
        if password != password2:
            raise forms.ValidationError('Password do not match')

        return password2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'placeholder': 'Enter email address'}
        )


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=150, widget=forms.TextInput(
        attrs={'placeholder': 'Email address'}
    ))

    def clean_email(self):
        email = self.cleaned_data['email']

        filter_email = UserBase.objects.filter(email=email).exists()

        if not filter_email:
            raise forms.ValidationError('No user account found with the email address you entered!')

        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter new password',
               'maxlength': '50', 'minlength': '5'}
    ))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter new password again',
               'maxlength': '50', 'minlength': '5'}
    ))


class UserEditForm(forms.ModelForm):
    username = forms.CharField(min_length=4, max_length=50, help_text='Required',
                               widget=forms.TextInput(attrs={'placeholder': 'Enter username'}))
    email = forms.EmailField(max_length=150, help_text='Required', error_messages={
        'required': 'Enter a valid email address'})
    mobile = PhoneNumberField(error_messages={'required': 'Enter a valid phone number'})


    class Meta:
        model = UserBase
        fields = ('email', 'username', 'mobile', 'profile_photo', )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['email'].required = True
        self.fields['mobile'].required = False
        self.fields['profile_photo'].required = False

    def clean_email(self):
        email = self.cleaned_data['email']

        filter_email = UserBase.objects.exclude(email=self.request.user.email).filter(email=email).exists()

        if filter_email:
            raise forms.ValidationError('Email address has already exists')

        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        filter_username = UserBase.objects.exclude(username=self.request.user.username).filter(username=username).exists()

        if filter_username:
            raise forms.ValidationError('Username already exists')

        filter_re = r"^(?=.{3,20}$)(?![_.-])(?!.*[_.]{2})[a-zA-Z0-9._-]+(?<![_.])$"

        if not re.search(filter_re, username):
            raise forms.ValidationError('You can only use letters, numbers and periods in the username')

        return username

    def clean_profile_photo(self):
        profile_photo = self.cleaned_data.get('profile_photo', None)

        if profile_photo:
            photo_path = pathlib.Path(str(profile_photo)).suffix

            if photo_path not in ['.jpg', '.jpeg', '.png']:
                raise forms.ValidationError('You can only upload images in jpg, jpeg or png formats')

        return profile_photo


class AddressEditForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update(
            {'minlength': '10'}
        )

        self.fields['phone'].widget.attrs.update(
            {'type': 'tel'}
        )

        self.fields['country'].widget.attrs.update(
            {'class': 'niceselect_option'}
        )

        self.fields['postal_code'].widget.attrs.update(
            {'min': 4}
        )

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']

        filter_first_name = r'^[a-zA-Z]{1,15}$'

        if not re.match(filter_first_name, first_name.lower()):
            raise forms.ValidationError('Please write your first name correctly')

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']

        filter_last_name = r'^[a-zA-Z]{1,15}$'

        if not re.match(filter_last_name, last_name.lower()):
            raise forms.ValidationError('Please write your last name correctly')

        return last_name

    def clean_company_name(self):
        company_name = self.cleaned_data['company_name']

        filter_company_name = r'^[a-zA-Z0-9 -]{1,50}$'

        if not re.match(filter_company_name, company_name.lower()):
            raise forms.ValidationError('Please write your company name correctly')

        return company_name

    def clean_email(self):
        email = self.cleaned_data['email'].lower()

        if UserBase.objects.exclude(email=self.request.user.email).filter(email=email).exists():
            raise forms.ValidationError('The e-mail address you entered belongs to another user')

        return email

    def clean_city(self):
        city = self.cleaned_data['city']

        filter_city = r'^[a-zA-Z ]{1,30}$'

        if not re.match(filter_city, city.lower()):
            raise forms.ValidationError('Please write city name correctly')

        return city

    def clean_address(self):
        address = self.cleaned_data['address']

        filter_address = r'^[a-zA-Z0-9 -.]{1,50}$'

        if not re.match(filter_address, address.lower()):
            raise forms.ValidationError('Please write your address correctly')

        return address
