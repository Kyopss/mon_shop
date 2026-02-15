from django.contrib import admin
from django.urls import path, include
from django.conf import settings             # <--- Important
from django.conf.urls.static import static   # <--- Important

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('cart/', include('cart.urls')),
    path('members/', include('members.urls')),
    path('payment/', include('payment.urls')),
]

# Ce bloc doit être collé tout à la fin, sans indentation (au bord gauche)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)