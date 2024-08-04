from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class PaymentTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase_order_id = models.CharField(max_length=255, unique=True)
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=50, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

