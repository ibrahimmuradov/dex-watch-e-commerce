from django.db import models
from django.contrib.auth import get_user_model
from services.mixin import DateMixin
from services.uploader import Uploader
from store.models import Watch


Users = get_user_model()

class Basket(DateMixin):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    watch = models.ForeignKey(Watch, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField()
    total_price = models.FloatField()

    def __str__(self):
        return self.watch.name

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'Basket'
        verbose_name_plural = 'Baskets'

