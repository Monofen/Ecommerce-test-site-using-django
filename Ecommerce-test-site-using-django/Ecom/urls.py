from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),  # Changed path to 'auth/'
    path('', include('products.urls')),    # Changed path to 'products/'
    path('', include('cart.urls', namespace='cart')),  # Changed path to 'cart/'
    path('payment/', include('payment.urls', namespace='payment')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
