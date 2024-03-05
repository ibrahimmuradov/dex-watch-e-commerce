from django.shortcuts import render
from .models import Faq, PrivacyPolicy, Term

def about(request):
    return render(request, 'about/about.html', {})

def faq(request):
    faqs = Faq.objects.all()

    return render(request, 'about/faq.html', {'faqs': faqs})

def privacy_policy(request):
    privacy_policies = PrivacyPolicy.objects.all()

    return render(request, 'about/privacy-policy.html', {'privacy_policies': privacy_policies})

def term_of_use(request):
    terms = Term.objects.all()

    return render(request, 'about/term-of-use.html', {'terms': terms})
