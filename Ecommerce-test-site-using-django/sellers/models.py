from django.db import models
from django.contrib.auth.models import User

class Sellers(models.Model):
    name = models.CharField(default="", blank=False, max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('products.Product', related_name='sellers_list') 
    khalti_api_code = models.CharField(default="", blank=False, max_length=150)
    facebook = models.URLField(default="", max_length=250, null=True, blank=True)
    instagram = models.URLField(default="", max_length=250, null=True, blank=True)
    youtube = models.URLField(default="", max_length=250, null=True, blank=True)
    extra = models.URLField(default="", max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name
