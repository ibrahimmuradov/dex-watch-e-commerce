from django.urls import path
from . import views

app_name = "watch"

urlpatterns = [
    path('', views.index, name='home'),
    path('shop/', views.shop, name='shop'),
    path('details/<int:id>/', views.details, name='details'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('delete-review/', views.delete_review, name='delete-review'),
]