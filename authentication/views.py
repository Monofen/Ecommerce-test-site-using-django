from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from products.models import Product
from django.http import HttpResponseRedirect
from .models import UserProfile
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from random import sample
from django.contrib.auth.models import User
from cart.models import Purchase
import random

def home(request):
    products = Product.objects.all()
    recommended_products = []
    recommended_type = None

    if request.user.is_authenticated:
        last_purchase = Purchase.objects.filter(user=request.user).order_by('-purchase_date').first()
        if last_purchase:
            category = last_purchase.product.category
            recommended_products = Product.objects.filter(category=category).exclude(id=last_purchase.product.id)[:4]
            recommended_type = "Next buy?"

    if not recommended_products:
        on_sale_products = Product.objects.filter(on_sale=True)
        best_sellers = Product.objects.annotate(num_purchases=Count('purchase')).order_by('-num_purchases')[:4]

        if random.choice([True, False]) and on_sale_products.exists():
            recommended_products = list(on_sale_products)[:3]
            recommended_type = "Sales"
        else:
            recommended_products = list(best_sellers)[:3]
            recommended_type = "Best Sellers"

    return render(request, 'index.html', {'products': products, 'recommended_products': recommended_products, 'recommended_type': recommended_type})

@login_required
def some_view(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        # Handle the missing profile, e.g., create one
        UserProfile.objects.create(user=request.user)
        profile = request.user.userprofile

def signup(request):
    if request.method == "POST":
        fname = request.POST['Firstname']
        lname = request.POST['Lastname']
        email = request.POST['Email']
        username = request.POST['Username']
        pass1 = request.POST['Password']
        pass2 = request.POST['Password1']
        address = request.POST.get('Address', '')
        phone_number = request.POST.get('PhoneNumber', '')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!!!")
            return redirect('home')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!!")
            return redirect('home')

        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('signup')
        
        if pass1 != pass2:
            messages.error(request, "Passwords did not match!!!")
            return redirect('signup')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()
        
        # Create or update UserProfile
        profile, created = UserProfile.objects.get_or_create(user=myuser)
        profile.address = address
        profile.phone_number = phone_number
        profile.save()
        
        messages.success(request, "Successful signup!! Please check your Email to activate your account.")

        # Welcome Email
        subject = "Welcome to Ecommerce site!!!"
        message = f"Hello {myuser.first_name}!! \nWelcome to Ecommerce shop!! \nThank you for visiting our website. \nWe have sent you a confirmation email, please confirm your email address to activate your account. \nThank you!!"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Confirmation
        current_site = get_current_site(request)
        email_subject = "Email confirmation for Ecommerce site."
        email_message = render_to_string('email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser),
        })
        email = EmailMessage(
            email_subject,
            email_message,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('signin')

    return render(request, "authentication/signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next')  

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next_url:  
                messages.success(request, 'Successfull login!!')
                return redirect(next_url)
            messages.success(request, 'Successfull login!!')
            return redirect('home') 
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'authentication/signin.html')


def signout(request):
    logout(request)
    messages.success(request, "Logged out Successfully!!")
    return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('home')
    else:
        return render(request, "activation_failed.html")