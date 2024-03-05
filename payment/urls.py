from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path('payment/<key>/', views.payment, name="payment"),
    path('invoice/<key>/', views.invoice, name="invoice"),
]
