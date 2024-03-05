from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Choice, Watch, WatchImage, Coupon, WatchReview


admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Choice)

class ImageInLine(admin.TabularInline):
    model = WatchImage
    extra = 1

class WatchAdmin(admin.ModelAdmin):
    inlines = (ImageInLine, )

admin.site.register(Watch, WatchAdmin)

admin.site.register(WatchImage)

admin.site.register(Coupon)

admin.site.register(WatchReview)