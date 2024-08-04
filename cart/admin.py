
from django.contrib import admin
from .models import CartItem, Purchase

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'purchase_date', 'total_price')
    search_fields = ('user__username', 'product__name')
    list_filter = ('purchase_date', 'product__category')

    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = 'Total Price'

admin.site.register(CartItem)
admin.site.register(Purchase, PurchaseAdmin)
