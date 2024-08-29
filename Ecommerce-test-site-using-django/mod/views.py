from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from authentication.models import UserProfile
from products.models import Category, Product, Sale, Coupon
from sellers.models import Sellers
from django.db.models import Q
from django.core.mail import send_mail
from django.template.loader import render_to_string
from datetime import datetime
from django.conf import settings
from django.utils import timezone

# Test function to check if the user is a superuser
def superuser_required(function):
    return user_passes_test(lambda u: u.is_superuser)(function)

@superuser_required
def admin_menu(request):
    return render(request, 'mod/admin_menu.html')

@superuser_required
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

@superuser_required
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

@superuser_required
def manage_applicants(request):
    applicants = Sellers.objects.filter(is_verified=False)

    return render(request, 'mod/manage_applicants.html', {'applicants': applicants})

@superuser_required
def review_application(request, seller_id):
    seller = get_object_or_404(Sellers, id=seller_id)
    
    if request.method == 'POST':
        if 'accept' in request.POST:
            # Handle acceptance logic
            seller.is_verified = True
            seller.save()
            
            # Send confirmation email
            subject = "Shop Application Approved"
            message = f"Hello {seller.user.first_name},\n\nYour shop '{seller.name}' has been approved and is now live on our platform."
            send_mail(subject, message, settings.EMAIL_HOST_USER, [seller.user.email], fail_silently=False)
            
            # Redirect after acceptance
            return redirect('manage_applicants')
        
        elif 'reject' in request.POST:
            # Redirect to rejection reason page
            return redirect('reject_application', seller_id=seller_id)

    return render(request, 'mod/review_application.html', {'seller': seller})

@superuser_required
def reject_application(request, seller_id):
    seller = get_object_or_404(Sellers, id=seller_id)
    
    if request.method == 'POST':
        reason = request.POST.get('reason', '').strip()
        if reason:
            # Handle rejection logic
            subject = "Shop Application Rejected"
            message = f"Hello {seller.user.first_name},\n\nYour shop '{seller.name}' has been rejected for the following reason:\n\n{reason}\n\nPlease contact our support team if you have any questions."
            send_mail(subject, message, settings.EMAIL_HOST_USER, [seller.user.email], fail_silently=False)
            
            # Optionally delete the seller if required
            seller.delete()
        
        # Redirect after rejection
        return redirect('manage_applicants')

    return render(request, 'mod/reject_application.html', {'seller': seller})

def send_sale_notification_email(sale):
    subject = "New Sale Started!"
    users = User.objects.all()
    for user in users:
        message = render_to_string('mod/sale_notification.html', {
            'user': user,
            'sale': sale,
            'start_date': sale.start_date,
            'end_date': sale.end_date,
        })
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )

@superuser_required
def create_sale(request):
    if request.method == 'POST':
        sale_type = request.POST.get('sale_type')
        percentage = request.POST.get('percentage')
        category_id = request.POST.get('category')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        start_date = timezone.make_aware(datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M'), timezone.get_current_timezone())
        end_date = timezone.make_aware(datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M'), timezone.get_current_timezone())

        category = get_object_or_404(Category, id=category_id) if category_id else None

        sale = Sale.objects.create(
            sale_type=sale_type,
            percentage=percentage,
            category=category,
            start_date=start_date,
            end_date=end_date
        )

        # Send email notifications
        send_sale_notification_email(sale)

        return redirect('admin_menu')

    categories = Category.objects.all()
    return render(request, 'mod/create_sale.html', {'categories': categories})

@superuser_required
def delete_sale(request):
    if request.method == 'POST':
        sale_id = request.POST.get('sale_id')
        sale = get_object_or_404(Sale, id=sale_id)
        sale.delete()
        return redirect('admin_menu')

    sales = Sale.objects.all()
    return render(request, 'mod/delete_sale.html', {'sales': sales})

@superuser_required
def add_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        discount_percentage = request.POST.get('discount_percentage')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        start_date = timezone.make_aware(datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M'), timezone.get_current_timezone())
        end_date = timezone.make_aware(datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M'), timezone.get_current_timezone())

        Coupon.objects.create(
            code=code,
            discount_percentage=discount_percentage,
            start_date=start_date,
            end_date=end_date
        )
        return redirect('admin_menu')

    return render(request, 'mod/add_coupon.html')

@superuser_required
def remove_coupon(request):
    if request.method == 'POST':
        coupon_id = request.POST.get('coupon_id')
        coupon = get_object_or_404(Coupon, id=coupon_id)
        coupon.delete()
        return redirect('admin_menu')

    coupons = Coupon.objects.all()
    return render(request, 'mod/remove_coupon.html', {'coupons': coupons})