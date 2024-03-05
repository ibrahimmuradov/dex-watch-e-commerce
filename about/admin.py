from django.contrib import admin
from .models import About, Faq, PrivacyPolicy, Term

admin.site.register(About)
admin.site.register(Faq)
admin.site.register(PrivacyPolicy)
admin.site.register(Term)
