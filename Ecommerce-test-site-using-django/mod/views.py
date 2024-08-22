from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from authentication.models import UserProfile
from sellers.models import Sellers
from django.db.models import Q
import hashlib
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from products.models import Category, CategorySale, Product
from django.contrib import messages
from decimal import Decimal

def admin_menu(request):
    return render(request, 'mod/admin_menu.html')

def manage_users(request):
    search_query = request.GET.get('search', '')
    if search_query:
        users = User.objects.filter(
            Q(username__icontains=search_query) |
            Q(userprofile__address__icontains=search_query) |
            Q(userprofile__phone_number__icontains=search_query)
        ).distinct()
    else:
        users = User.objects.all()

    return render(request, 'mod/manage_users.html', {'users': users})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        reason = request.POST.get('reason')
        custom_reason = request.POST.get('custom_reason', '')
        
        if reason == 'custom':
            reason = custom_reason

        subject = "Your profile has been deleted."
        message = f"Hello {user.first_name},\n\nYour profile has been deleted from our site for the following reason:\n\n{reason}\n\nIf you believe this is a mistake, please contact our support team."

        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)
        
        user.delete()
        return redirect('manage_users')

    return redirect('manage_users')

def manage_sales(request): 
    parent_categories = Category.objects.filter(parent__isnull=True)
    return render(request, 'mod/manage_sales.html', {'parent_categories': parent_categories})



def set_sale(request, category_id, percentage):
    category = get_object_or_404(Category, id=category_id)

    # Validate percentage
    if not (0 <= percentage <= 100):
        messages.error(request, 'Percentage must be between 0 and 100.')
        return redirect('manage_users')

    # Convert percentage to Decimal
    percentage_decimal = Decimal(percentage)

    # Update or create the CategorySale entry
    category_sale, created = CategorySale.objects.update_or_create(
        category=category,
        defaults={'percentage': percentage_decimal}
    )

    # List of categories to update including subcategories
    categories_to_update = [category] + list(category.get_all_subcategories())
    
    for cat in categories_to_update:
        # Update or create the CategorySale entry for each category
        CategorySale.objects.update_or_create(
            category=cat,
            defaults={'percentage': percentage_decimal}
        )

        # Update sale price for all products in this category
        products = Product.objects.filter(category=cat)
        for product in products:
            original_price = product.price
            if percentage > 0:
                percentage_decimal = Decimal(percentage) / Decimal(100)
                new_sale_price = original_price - (percentage_decimal * original_price)
                product.sale_price = new_sale_price
                product.on_sale = True
            else:
                product.sale_price = original_price
                product.on_sale = False
            product.save()

    if created:
        messages.success(request, f'Sale of {percentage}% has been set for {category.name}.')
    else:
        messages.success(request, f'Sale percentage updated to {percentage}% for {category.name}.')

    return redirect('manage_sales')




