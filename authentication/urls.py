from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from products import views as product_views
from authentication import views as auth_views
from cart import views as cart_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.home, name='home'),
    path('signup/', auth_views.signup, name='signup'),
    path('signin/', auth_views.signin, name='signin'),
    path('signout/', auth_views.signout, name='signout'),
    path('activate/<uidb64>/<token>/', auth_views.activate, name='activate'),
    path('product/<int:product_id>/', product_views.product_detail, name='product_detail'),
    path('product/<int:product_id>/add_comment/', product_views.add_comment, name='add_comment'),
    path('profile/', cart_views.profile, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)