from django.db import models
from django.contrib.auth import get_user_model
from services.mixin import DateMixin
from ckeditor.fields import RichTextField
from phonenumber_field.modelfields import PhoneNumberField


Users = get_user_model()

class About(DateMixin):
    title = models.CharField(max_length=500, null=True)
    header = models.TextField()
    text = models.TextField()
    address = models.CharField(max_length=200, null=True)
    mail = models.EmailField(blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)


    def __str__(self):
        return 'About Text'

    class Meta:
        verbose_name = 'about'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.__class__.objects.exclude(id=self.id).delete()


class Faq(DateMixin):
    question = models.CharField(max_length=600)
    answer = models.TextField()

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'faq'
        verbose_name_plural = 'faqs'
        ordering = ('created_at', )


class Term(DateMixin):
    title = models.CharField(max_length=500)
    description = RichTextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Term'
        verbose_name_plural = 'Terms'
        ordering = ('created_at', )


class PrivacyPolicy(DateMixin):
    title = models.CharField(max_length=500)
    description = RichTextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Privacy Policy'
        verbose_name_plural = 'Privacy Policies'
        ordering = ('created_at',)


