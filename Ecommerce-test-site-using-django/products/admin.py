from django.contrib import admin
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Category, Product, ProductImage, ElectronicProduct, Comment, Rating

@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_electronics']
    search_fields = ['name']

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

class ElectronicProductInline(admin.StackedInline):
    model = ElectronicProduct
    can_delete = False
    verbose_name_plural = 'Electronic Features'
    fk_name = 'product'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    inlines = [ProductImageInline]

    def get_inline_instances(self, request, obj=None):
        inline_instances = super().get_inline_instances(request, obj)
        if obj and obj.category.is_electronics:
            inline_instances.append(ElectronicProductInline(self.model, self.admin_site))
        return inline_instances

@receiver(post_save, sender=Product)
def create_or_update_electronic_product(sender, instance, created, **kwargs):
    if instance.category.is_electronics:
        ElectronicProduct.objects.get_or_create(product=instance)
    else:
        if hasattr(instance, 'electronicproduct'):
            instance.electronicproduct.delete()

@admin.register(Comment)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['product','user', 'parent']
    search_fields = ['user']

class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'stars', 'created_at')

admin.site.register(Rating, RatingAdmin)