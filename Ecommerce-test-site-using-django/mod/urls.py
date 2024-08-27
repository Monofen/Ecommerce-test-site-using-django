from django.urls import path
from . import views

urlpatterns = [
    path('admin-menu/', views.admin_menu, name='admin_menu'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('manage_applicants/', views.manage_applicants, name='manage_applicants'),
    path('review_application/<int:seller_id>/', views.review_application, name='review_application'),
    path('reject_application/<int:seller_id>/', views.reject_application, name='reject_application'),
    path('create_sale/', views.create_sale, name='create_sale'),
    path('delete_sale/', views.delete_sale, name='delete_sale'),
]
