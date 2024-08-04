from .models import Category, Product

def category_data(request):
    categories = Category.objects.filter(parent=None)
    return {
        'categoryData': categories,
    }

def product_data(request):
    productData = {category.id: Product.objects.filter(category=category) for category in Category.objects.all()}
    return {
        'productData': productData,
    }