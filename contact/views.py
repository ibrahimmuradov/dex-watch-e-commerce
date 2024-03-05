from django.shortcuts import render, redirect
from .forms import ContactForm
from django.conf import settings
from django.core.mail import send_mail

def contact(request):
    contact_form = ContactForm()

    if request.method == "POST":
        contact_form = ContactForm(request.POST or None)

        if contact_form.is_valid():
            contact_form.save()

            subject = contact_form.cleaned_data.get('subject')
            message = contact_form.cleaned_data.get('message')

            # sending mail
            send_mail(
                subject,
                message,
                settings.EMAIL_USER_USER,
                ['yourmail@mail.com'],
                fail_silently=False,
            )

            return redirect("contact:contact")

    context = {
        "contactForm": contact_form
    }

    return render(request, 'contact/contact.html', context)
