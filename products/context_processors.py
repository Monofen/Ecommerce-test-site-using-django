# context_processors.py
from .models import Category

def categories(request):
    return {
        'categoryData': Category.objects.filter(parent__isnull=True)
    }