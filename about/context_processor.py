from .models import About


def about_context_processor(request):
    about = About.objects.first()

    return {"about": about}
