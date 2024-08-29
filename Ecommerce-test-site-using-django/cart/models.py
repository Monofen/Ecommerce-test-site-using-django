from django.db import models
from django.contrib.auth.models import User
from products.models import Product, Coupon

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)

    @property
    def item_total(self):
        price = self.product.sale_price if self.product.on_sale else self.product.price
        if self.coupon and self.coupon.is_active():
            discount = self.coupon.discount_percentage / 100
            price *= (1 - discount)
        return price * self.quantity

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    @property
    def total_price(self):
        return (self.product.sale_price if self.product.on_sale else self.product.price) * self.quantity
