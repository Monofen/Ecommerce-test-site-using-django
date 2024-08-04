from django.db import models
import datetime
from django.contrib.auth.models import User

class Category(models.Model):
    search_field = ('name',)
    name = models.CharField(max_length=50, default='', blank=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    is_electronics = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'

    def get_children(self):
        return Category.objects.filter(parent=self)

    def get_all_subcategories(self):
        """Recursively get all subcategories"""
        subcategories = list(self.get_children())
        for subcategory in subcategories:
            subcategories.extend(subcategory.get_all_subcategories())
        return subcategories
    
class Product(models.Model):
    search_field = ('name',)
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0,decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=550, blank=True, null=True)
    on_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0,decimal_places=2, max_digits=6)

    def __str__(self):
        return self.name
    
class ElectronicProduct(models.Model):
    SCREEN_CHOICES = [
        ('LCD','LCD'),
        ('LED','LED'),
        ('OLED','OLED'),
        ('AMOLED','AMOLED'),
    ]
    RAM_CHOICES = [
        ('2GB','2GB'),
        ('4GB','4GB'),
        ('8GB','8GB'),
        ('16GB','16GB'),
    ]
    product = models.OneToOneField(Product, related_name='electronic_features', on_delete=models.CASCADE)
    screen = models.CharField(max_length=30, choices=SCREEN_CHOICES)
    ram = models.CharField(max_length=15, choices=RAM_CHOICES)

    def __str__(self):
        return f'{self.product.name} Electronics Features'
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/product/')

    def __str__(self):
        return f'{self.product.name} Image'
    
class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment by {self.user.first_name} {self.user.last_name} on {self.product}'
    
class Rating(models.Model):
    product = models.ForeignKey(Product, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.PositiveIntegerField()
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='rating_images/', null=True, blank=True)

    def __str__(self):
        return f'Rating by {self.user.username} on {self.product.name}'
