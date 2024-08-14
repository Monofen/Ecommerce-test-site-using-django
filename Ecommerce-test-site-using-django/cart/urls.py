from django.urls import path
from .views import order_confirmation, add_to_cart, cart_summary, purchase_history, update_quantity, delete_item, add_product, add_electronics_features, edit_product, delete_product, update_photo, edit_shop, delete_shop, confirm_delete_shop
from django.contrib.auth import views as auth_views
from . import views

app_name = 'cart'

urlpatterns = [
    path('order_confirmation/<int:product_id>/', order_confirmation, name='order_confirmation'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('cart_summary/', cart_summary, name='cart_summary'),
    path('purchase_history/', purchase_history, name='purchase_history'),
    path('update_quantity/<int:item_id>/', update_quantity, name='update_quantity'),
    path('delete_item/<int:item_id>/', delete_item, name='delete_item'),
    path('add-product/', add_product, name='add_product'),
    path('add-electronics-features/<int:product_id>/', add_electronics_features, name='add_electronics_features'),
    path('product/<int:pk>/edit/', edit_product, name='edit_product'),
    path('product/<int:pk>/delete/', delete_product, name='delete_product'),
    path('update_photo/', update_photo, name='update_photo'),
    path('edit-shop/', edit_shop, name='edit_shop'),
    path('delete-shop/', delete_shop, name='delete_shop'),
    path('confirm-delete-shop/<str:verification_code>/<int:seller_pk>/', confirm_delete_shop, name='confirm_delete_shop'),
    path('send-change-password-email/', views.send_change_password_email, name='send_change_password_email'),
    path('reset/<uidb64>/<token>/confirm/', views.change_password_confirm, name='change_password_confirm'),
    path('reset/<uidb64>/<token>/change/', views.password_change_form, name='password_change_form'),
]
