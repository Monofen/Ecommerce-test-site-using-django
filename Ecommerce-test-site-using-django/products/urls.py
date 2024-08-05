from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:pk>/', views.CategoryView.as_view(), name='category'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/comment/', views.add_comment, name='add_comment'),
    path('product/<int:product_id>/ratings/', views.product_ratings, name='product_ratings'),
    path('api/<str:product_name>/', views.product_detail_by_name, name='product_detail_by_name'),
    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('rating/edit/<int:rating_id>/', views.edit_rating, name='edit_rating'),
    path('rating/delete/<int:rating_id>/', views.delete_rating, name='delete_rating'),
]
