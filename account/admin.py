from django.contrib import admin
from .models import UserBase, Address

admin.site.register(UserBase)
admin.site.register(Address)
