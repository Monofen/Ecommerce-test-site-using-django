from django.shortcuts import render
from django.views.generic import DetailView
from .models import Product, Category, Comment, Rating
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import Purchase
from .forms import RatingForm, CommentForm
from random import sample
from django.contrib.auth.models import User
from django.http import JsonResponse

def index(request):
    products = Product.objects.all()
    recommended_products = []
    if request.user.is_authenticated:
        last_purchase = Purchase.objects.filter(user=request.user).order_by('-purchase_date').first()
        if last_purchase:
            category = last_purchase.product.category
            recommended_products = Product.objects.filter(category=category).exclude(id=last_purchase.product.id)[:4]
    if not recommended_products:
        on_sale_products = Product.objects.filter(on_sale=True)
        best_sellers = sample(list(Product.objects.all()), 4)  
        recommended_products = list(on_sale_products) + best_sellers[:4 - len(on_sale_products)]
        
    return render(request, 'index.html', {'products': products, 'recommended_products': recommended_products})

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'products/products_detail.html', {'product': product})

class CategoryView(DetailView):
    model = Category
    template_name = 'products/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        
        
        products = Product.objects.filter(category=category)
        
        
        all_subcategories = category.get_all_subcategories()
        products |= Product.objects.filter(category__in=all_subcategories)
        
        context['products'] = products
        context['subcategories'] = category.get_children()
        return context


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    comments = product.comments.filter(parent=None)
    ratings = product.ratings.all()

    has_purchased = False
    user_has_rated = False
    if request.user.is_authenticated:
        has_purchased = Purchase.objects.filter(user=request.user, product=product).exists()
        user_has_rated = Rating.objects.filter(user=request.user, product=product).exists()

    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    if request.method == 'POST' and not user_has_rated:
        rating_form = RatingForm(request.POST, request.FILES)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.user = request.user
            rating.product = product
            rating.save()
            return redirect('product_detail', product_id=product.id)
    else:
        rating_form = RatingForm()

    context = {
        'product': product,
        'comments': comments,
        'ratings': ratings,
        'has_purchased': has_purchased,
        'user_has_rated': user_has_rated,
        'rating_form': rating_form,
        'related_products': related_products,
        'star_range': range(1, 6),
    }
    return render(request, 'products/products_detail.html', context)

@login_required
def edit_rating(request, rating_id):
    rating = get_object_or_404(Rating, pk=rating_id)
    if request.user != rating.user:
        return redirect('product_ratings', product_id=rating.product.id)

    if request.method == 'POST':
        form = RatingForm(request.POST, request.FILES, instance=rating)
        if form.is_valid():
            form.save()
            return redirect('product_ratings', product_id=rating.product.id)
    else:
        form = RatingForm(instance=rating)

    return render(request, 'products/edit_rating.html', {'form': form, 'rating': rating})

@login_required
def delete_rating(request, rating_id):
    rating = get_object_or_404(Rating, pk=rating_id)
    if request.user == rating.user:
        rating.delete()
    return redirect('product_ratings', product_id=rating.product.id)

@login_required
def add_comment(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        text = request.POST.get('comment')
        parent_id = request.POST.get('parent_id')
        parent_comment = None

        if parent_id:
            parent_comment = get_object_or_404(Comment, pk=parent_id)

        Comment.objects.create(
            product=product,
            user=request.user,
            text=text,
            parent=parent_comment
        )
        return redirect('product_detail', product_id=product_id)
    
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.user:
        return redirect('product_detail', product_id=comment.product.id)
    
    if request.method == 'POST':
        comment.text = request.POST.get('comment')
        comment.save()
        return redirect('product_detail', product_id=comment.product.id)

    return redirect('product_detail', product_id=comment.product.id)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.user:
        comment.delete()
    return redirect('product_detail', product_id=comment.product.id)
    
def product_ratings(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    comments = product.comments.filter(parent=None)
    ratings = product.ratings.all()
    
    context = {
        'product': product,
        'comments': comments,
        'ratings': ratings,
    }
    return render(request, 'products/product_rating.html', context)

def product_detail_by_name(request, product_name):
    product = get_object_or_404(Product, name=product_name)
    comments = product.comments.filter(parent=None)
    ratings = product.ratings.all()  

    has_purchased = False
    if request.user.is_authenticated:
        has_purchased = Purchase.objects.filter(user=request.user, product=product).exists()
    
    
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]  
    
    if request.method == 'POST':
        rating_form = RatingForm(request.POST, request.FILES)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.user = request.user
            rating.product = product
            rating.save()
            return redirect('product_detail', product_id=product.id)
    else:
        rating_form = RatingForm()

    context = {
        'product': product,
        'comments': comments,
        'ratings': ratings,  
        'has_purchased': has_purchased,
        'rating_form': rating_form,
        'related_products': related_products,  
    }
    return render(request, 'products/products_detail.html', context)
