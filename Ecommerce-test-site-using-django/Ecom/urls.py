from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),  
    path('', include('products.urls')),    
    path('', include('cart.urls', namespace='cart')),  
    path('payment/', include('payment.urls', namespace='payment')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
