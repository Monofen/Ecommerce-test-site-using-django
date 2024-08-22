from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from authentication.models import UserProfile
from sellers.models import Sellers
from django.db.models import Q
import hashlib
from django.core.mail import send_mail, EmailMessage
from django.conf import settings

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
