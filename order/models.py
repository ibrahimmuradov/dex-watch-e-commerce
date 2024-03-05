from django.db import models
from services.mixin import DateMixin
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from store.models import Watch
from services.generator import Generator
from store.models import Coupon


Users = get_user_model()

class Order(DateMixin):
    invoice_id = models.PositiveIntegerField(unique=True, null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, related_name='user_order')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=270, blank=True)
    address = models.CharField(max_length=300)
    country = models.ForeignKey('order.Country', on_delete=models.SET_NULL, null=True, blank=True, related_name='country')
    city = models.CharField(max_length=150)
    phone = PhoneNumberField()
    postal_code = models.PositiveIntegerField()
    coupon_discount = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, related_name='coupon')
    coupon_discount_value = models.FloatField(null=True, blank=True)
    subtotal = models.FloatField(null=True)
    total_paid = models.FloatField()
    verification_key = models.CharField(max_length=25, null=True, blank=True)
    billing_status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.invoice_id)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderItem(DateMixin):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    watch = models.ForeignKey(Watch, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    price = models.FloatField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.watch.name} -- {self.order.invoice_id}'

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'


class Country(DateMixin):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('created_at', )
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
