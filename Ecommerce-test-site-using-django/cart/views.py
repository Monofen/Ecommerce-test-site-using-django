from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product, Category, ProductImage, ElectronicProduct
from sellers.models import Sellers
from cart.models import CartItem, Purchase
from django.contrib import messages
from authentication.models import UserProfile

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
        sale_price = request.POST.get('sale_price', 0)
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
            sale_price=sale_price,
        )

        product.sellers.set([seller])

        if 'product_image' in request.FILES:
            images = request.FILES.getlist('product_image')
            for image in images:
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