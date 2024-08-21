from django.urls import path
from .views import create_shop

urlpatterns = [
    path('create-shop/', create_shop, name='create_shop'),
]
