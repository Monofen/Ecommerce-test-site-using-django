from django.contrib import admin
from .models import Sellers

@admin.register(Sellers)
class SellersADmin(admin.ModelAdmin):
    list_display = ['name']
