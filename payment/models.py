from django.db import models
from services.mixin import DateMixin
from order.models import Order

class Payment(DateMixin):
    name = models.CharField(max_length=30)
    number = models.CharField(max_length=20)
    code = models.PositiveIntegerField()
    date = models.DateTimeField()
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
