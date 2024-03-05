from django.urls import path
from . import views

app_name = 'about'

urlpatterns = [
    path('about/', views.about, name="about"),
    path('faq/', views.faq, name="faq"),
    path('privacy-policy/', views.privacy_policy, name="privacy-policy"),
    path('term-of-use/', views.term_of_use, name="term-of-use"),
]