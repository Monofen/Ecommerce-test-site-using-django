from django.urls import path
from .views import order_confirmation, add_to_cart, cart_summary, purchase_history, update_quantity, delete_item, add_product, add_electronics_features

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
]
