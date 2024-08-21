from django.urls import path
from . import views

urlpatterns = [
    path('admin-menu/', views.admin_menu, name='admin_menu'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
]
