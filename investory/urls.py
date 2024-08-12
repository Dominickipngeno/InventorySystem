from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('per_product/<int:pk>', views.per_product, name='per_product'),
    path('logout/', views.custom_logout, name='logout'),
    path('add_products/', views.add_products, name='add_products'),
    path('delete/<int:pk>/', views.delete_inventory, name='delete_inventory'),
    path('update/<int:pk>/', views.inventory_update, name='update_inventory'),
    path('dashboard/', views.dashbaord, name='dashboard'),
]   