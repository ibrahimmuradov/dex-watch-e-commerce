from django.urls import path
from . import views

app_name = 'basket'

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('basket-add/', views.basket_add, name='basket_add'),
    path('basket-delete/', views.basket_delete, name='basket_list'),
    path('subtotal/', views.subtotal, name='subtotal'),
    path('remove-coupon/', views.remove_coupon, name='remove-coupon'),
]