from django import forms
from store.models import Coupon


class CouponForm(forms.ModelForm):
    code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Coupon code'}))

    class Meta:
        model = Coupon
        fields = ('code', )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        code = self.cleaned_data.get('code')

        if not self.request.user.is_authenticated:
            raise forms.ValidationError('You must log in to your account')
        elif not Coupon.objects.filter(code=code).exists():
            raise forms.ValidationError('Code not found')
        elif Coupon.objects.filter(code=code, status='Deactivate').exists():
            raise forms.ValidationError('Code is not active')
        elif Coupon.objects.filter(code=code, access='Inaccessible').exists():
            raise forms.ValidationError('Code is inaccessible')

        return self.cleaned_data