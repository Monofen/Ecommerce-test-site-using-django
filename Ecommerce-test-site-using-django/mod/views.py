from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from authentication.models import UserProfile
from sellers.models import Sellers
from django.db.models import Q
import hashlib

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
        user.delete()
        return redirect('manage_users')
    return redirect('manage_users')