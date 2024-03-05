from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('payment/', include('payment.urls')),
    path('order/', include('order.urls')),
    path('basket/', include('basket.urls')),
    path('contact/', include('contact.urls')),
    path('account/', include('account.urls')),
    path('', include('about.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
