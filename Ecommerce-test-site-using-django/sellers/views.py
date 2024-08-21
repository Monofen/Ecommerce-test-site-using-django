from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Sellers
from .forms import SellerForm
from django.contrib import messages

@login_required
def create_shop(request):
    seller = Sellers.objects.filter(user=request.user).first()

    if seller:
        messages.warning(request, "You already have a shop.")
        return redirect('profile')  

    if request.method == 'POST':
        form = SellerForm(request.POST, request.FILES)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.user = request.user
            shop.save()
            messages.success(request, "Shop created successfully! you will be sent a email after the shop has been verified then you can start selling.")
            return redirect('profile')  
    else:
        form = SellerForm()

    return render(request, 'sellers/create_shop.html', {'form': form})
