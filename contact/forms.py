from django import forms
from contact.models import Contact


class ContactForm(forms.ModelForm):
    name = forms.CharField(max_length=80, min_length=3)
    email = forms.EmailField(max_length=150, min_length=7)
    subject = forms.CharField(max_length=80, min_length=3)
    message = forms.CharField(max_length=800, min_length=5, widget=forms.Textarea(
        attrs={"class": "form-control2"}
    ))

    class Meta:
        model = Contact
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data.get('name', None)

        if name and not name.replace(" ", "").isalpha():
            raise forms.ValidationError('You must use only letters in the name')

        return name


