from django import forms
from .models import Order
import re
from django.contrib.auth import get_user_model

Users = get_user_model()

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'company_name', 'email',
                  'address', 'country', 'city', 'phone', 'postal_code', )

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

        if Users.objects.exclude(email=self.request.user.email).filter(email=email).exists():
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

        filter_address = r'^[a-zA-Z0-9 -]{1,50}$'

        if not re.match(filter_address, address.lower()):
            raise forms.ValidationError('Please write your address correctly')

        return address
