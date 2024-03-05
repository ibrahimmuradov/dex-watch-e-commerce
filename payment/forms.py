from django import forms
from .models import Payment
import re


class PaymentForm(forms.ModelForm):
    code = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control", "maxlength": 3}
    ))
    class Meta:
        model = Payment
        fields = ('number', 'code', 'name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['number'].widget.attrs.update({
            "class": "form-control", "maxlength": 19, "autocomplete": "off",
        })
        self.fields['name'].widget.attrs.update({
            "class": "form-control text-uppercase", "maxlength": 30,
        })

    def clean_number(self):
        number = self.cleaned_data['number'].replace(" ", "")

        if len(number) != 16 or not number.isdigit():
            raise forms.ValidationError("Your credit card number is incorrect")

        return int(number)

    def clean_name(self):
        name = self.cleaned_data['name'].lower()

        filter_name = r'^[a-zA-Z ]{1,30}$'

        if not re.match(filter_name, name):
            raise forms.ValidationError("Please write name correctly")

        return name

    def clean_code(self):
        code = self.cleaned_data['code']

        if len(code) != 3 or not code.isdigit():
            raise forms.ValidationError("Please write CVV correctly")

        return code
