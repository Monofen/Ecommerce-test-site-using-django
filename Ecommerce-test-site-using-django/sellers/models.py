import hashlib
from django.db import models
from django.contrib.auth.models import User

class Sellers(models.Model):
    name = models.CharField(default="", blank=False, max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('products.Product', related_name='sellers_list')
    khalti_api_code = models.CharField(default="", blank=False, max_length=150)
    citizenship = models.ImageField(upload_to='uploads/owner_detail/', null=True, blank=True)
    cit_num = models.IntegerField(null=True, blank=True)
    owner_pic = models.ImageField(upload_to='uploads/owner_detail/', null=True, blank=True)
    registration_certificate = models.ImageField(upload_to='uploads/owner_detail/', null=True, blank=True)
    pan_number = models.IntegerField(null=True, blank=True)
    pan_pic = models.ImageField(upload_to='uploads/owner_detail/', null=True, blank=True)
    facebook = models.URLField(default="", max_length=250, null=True, blank=True)
    instagram = models.URLField(default="", max_length=250, null=True, blank=True)
    youtube = models.URLField(default="", max_length=250, null=True, blank=True)
    extra = models.URLField(default="", max_length=250, null=True, blank=True)
    is_verified = models.BooleanField(default=False) 

    def save(self, *args, **kwargs):
        super(Sellers, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
