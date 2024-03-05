from django import forms
from .models import WatchReview
from order.models import Order, OrderItem

class ReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Write a review'}))

    class Meta:
        model = WatchReview
        fields = ('rating', 'review', )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.id = kwargs.pop('id', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        if not self.request.user.is_authenticated:
            raise forms.ValidationError('To write a review, you must be logged in to your account and have purchased this product')
        elif WatchReview.objects.filter(user=self.request.user, watch__id=self.id).exists():
            raise forms.ValidationError('You can only write one review!')
        elif not OrderItem.objects.filter(user=self.request.user, watch__id=self.id).exists():
            raise forms.ValidationError('You must have purchased the product to write a review')
