from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from products.models import Product, Category, ProductImage, ElectronicProduct
from sellers.models import Sellers
from cart.models import CartItem, Purchase
from django.contrib import messages
from authentication.models import UserProfile
from .forms import ProductForm
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils.translation import gettext as _
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm

@login_required
def update_photo(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        if 'photo' in request.FILES:
            profile.photo = request.FILES['photo']
            profile.save()
            messages.success(request, 'Profile photo updated successfully!')
        else:
            messages.error(request, 'No photo uploaded.')
        return redirect('profile')

    return redirect('profile')

@login_required
def order_confirmation(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 0))
        if quantity > 0:
            CartItem.objects.create(user=request.user, product=product, quantity=quantity)
            messages.success(request, 'Product added to cart successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Quantity must be greater than 0.')
    return render(request, 'cart/order_confirmation.html', {'product': product})

@login_required
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    return redirect('cart:order_confirmation', product_id=product_id)

@login_required
def cart_summary(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        
        total_cart_price = sum(item.quantity * (item.product.sale_price if item.product.on_sale else item.product.price) for item in cart_items)
        
        context = {
            'cart_items': cart_items,
            'total_cart_price': total_cart_price,
        }
        
        return render(request, 'cart/cart_summary.html', context)
    else:
        return redirect('login')

@login_required
def update_quantity(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 0))
        if quantity > 0:
            cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart item updated successfully!')
        else:
            messages.error(request, 'Quantity must be greater than 0.')
    return redirect('cart:cart_summary')

@login_required
def delete_item(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        cart_item.delete()
        messages.success(request, 'Cart item deleted successfully!')
    return redirect('cart:cart_summary')

@login_required
def purchase_history(request):
    purchases = Purchase.objects.filter(user=request.user)
    return render(request, 'cart/purchase_history.html', {'purchases': purchases})

@login_required
def profile(request):
    profile = UserProfile.objects.get(user=request.user)
    seller = Sellers.objects.filter(user=request.user).first()
    products = Product.objects.filter(sellers__user=request.user)

    if request.method == 'POST':
        if not seller:
            shop_name = request.POST.get('shop_name')
            khalti_api_code = request.POST.get('khalti_api_code')
            Sellers.objects.create(
                name=shop_name,
                user=request.user,
                khalti_api_code=khalti_api_code
            )
            messages.success(request, 'Shop created successfully!')
            return redirect('profile')

    categories = Category.objects.all()

    context = {
        'profile': profile,
        'seller': seller,
        'categories': categories,
        'products': products,  # Include the products in the context
    }
    return render(request, 'cart/profile.html', context)

@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('product_name')
        price = request.POST.get('product_price')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        on_sale = 'on_sale' in request.POST
        sale_price = request.POST.get('sale_price') if on_sale else None
        
        try:
            seller = Sellers.objects.get(user=request.user)
        except Sellers.DoesNotExist:
            return redirect('profile')

        category = get_object_or_404(Category, id=category_id)

        product = Product.objects.create(
            name=name,
            price=price,
            category=category,
            description=description,
            on_sale=on_sale,
            sale_price=sale_price,  # Set sale_price only if on_sale is True
        )

        product.sellers.set([seller])

        if 'product_images' in request.FILES:
            for image in request.FILES.getlist('product_images'):
                ProductImage.objects.create(product=product, image=image)

        if category.is_electronics:
            return redirect('cart:add_electronics_features', product_id=product.id)

        return redirect('profile')

    categories = Category.objects.all()
    return render(request, 'cart/add_product.html', {'categories': categories})

@login_required
def add_electronics_features(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        electronic_product, created = ElectronicProduct.objects.get_or_create(product=product)
        electronic_product.screen = request.POST.get('screen')
        electronic_product.ram = request.POST.get('ram')
        electronic_product.save()
        return redirect('profile')

    return render(request, 'cart/add_electronics_features.html', {'product_id': product_id})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product, product=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product detail changed!!")
            return redirect('profile')
    else:
        form = ProductForm(instance=product, product=product)

    return render(request, 'edit_product.html', {'form': form, 'product': product})


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product removed!!")
        return redirect('profile')  

    return render(request, 'delete_product.html', {'product': product})

@login_required
def edit_shop(request):
    seller = get_object_or_404(Sellers, user=request.user)
    
    if request.method == 'POST':
        new_name = request.POST.get('shop_name')
        seller.name = new_name
        seller.save()
        messages.success(request, 'Shop name updated successfully!')
        return redirect('profile')
    
    return render(request, 'cart/edit_shop.html', {'seller': seller})

@login_required
def delete_shop(request):
    seller = get_object_or_404(Sellers, user=request.user)
    
    if request.method == 'POST':
        generate_token = PasswordResetTokenGenerator()
        verification_code = generate_token.make_token(request.user)
        
        delete_confirmation_url = request.build_absolute_uri(
            reverse("cart:confirm_delete_shop", args=[verification_code, seller.pk])    
        )
        
        send_mail(
            'Delete Shop Verification',
            f'Click the link to confirm deletion: {delete_confirmation_url}',
            'no-reply@example.com',
            [request.user.email],
            fail_silently=False,
        )
        
        messages.info(request, 'A verification email has been sent to you.')
        return redirect('profile')
    
    return redirect('profile')

@login_required
def confirm_delete_shop(request, verification_code, seller_pk):
    # Validate the verification code/token and seller_pk
    seller = get_object_or_404(Sellers, pk=seller_pk, user=request.user)

    # Check if the verification code is valid
    if not PasswordResetTokenGenerator().check_token(request.user, verification_code):
        messages.error(request, 'Invalid or expired verification link.')
        return redirect('profile')

    # Retrieve all products related to the seller
    products = seller.products_list.all()

    # Delete related data for each product
    for product in products:
        # Delete related electronic features
        if hasattr(product, 'electronic_features'):
            product.electronic_features.delete()
        
        # Delete related images
        product.productimage_set.all().delete()
        
        # Delete related comments
        product.comments.all().delete()
        
        # Delete the product itself
        product.delete()

    # Delete the seller
    seller.delete()

    messages.success(request, 'Your shop and all related products have been deleted.')
    return redirect('profile')

@login_required
def send_change_password_email(request):
    user = request.user
    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    current_site = get_current_site(request)
    mail_subject = _('Change your password')
    message = render_to_string('cart/change_password_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': uid,
        'token': token,
        'protocol': 'https' if request.is_secure() else 'http',
    })
    send_mail(
        mail_subject, 
        message, 
        settings.DEFAULT_FROM_EMAIL, 
        [user.email]
    )
    messages.success(request, _('A confirmation email has been sent to your email address.'))
    return redirect('profile')

def change_password_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    token_generator = PasswordResetTokenGenerator()
    
    if user is not None and token_generator.check_token(user, token):
        # Redirect to password_change_form view
        return redirect('cart:password_change_form', uidb64=uidb64, token=token)
    else:
        messages.error(request, _('The password reset link is invalid, possibly because it has already been used.'))
        return redirect('profile')

def password_change_form(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    token_generator = PasswordResetTokenGenerator()
    
    if user is not None and token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)  # Keep the user logged in
                messages.success(request, 'Your password has been set successfully!')
                return redirect('profile')
        else:
            form = SetPasswordForm(user)
        return render(request, 'cart/password_change_form.html', {'form': form})
    else:
        messages.error(request, 'The password reset link is invalid or has expired.')
        return redirect('profile')

