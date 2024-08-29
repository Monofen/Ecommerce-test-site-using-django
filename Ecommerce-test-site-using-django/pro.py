from django.utils import timezone
from products.models import Sale, Category
from anyio import current_time

current_time = timezone.now()
tv_category = Category.objects.get(name='TV')
tv_sales = Sale.objects.filter(category=tv_category, start_date__lte=current_time, end_date__gte=current_time, sale_type='category')

if tv_sales.exists():
    print(f"Sale found for TV category: {tv_sales.first().percentage}% off")
else:
    print("No sale found for TV category.")
