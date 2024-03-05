from django.db import models
from services.mixin import DateMixin

class Contact(DateMixin):
    name = models.CharField(max_length=80)
    email = models.EmailField()
    subject = models.CharField(max_length=80)
    message = models.TextField()

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return self.name