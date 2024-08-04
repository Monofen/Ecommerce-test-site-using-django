from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from cart.models import CartItem, Purchase
from django.contrib import messages

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
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'cart/cart.html', {'cart_items': cart_items})
