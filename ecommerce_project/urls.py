from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from shop import views
from shop.views import (
    product_list, 
    register_view, 
    user_board, 
    cart_detail, 
    cart_add, 
    checkout
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', product_list, name='home'),
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', checkout, name='checkout'),
    
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    path('userboard/', user_board, name='user_board'),
    path('order/update/<int:order_id>/<str:new_status>/', views.update_order_status, name='update_order_status'),
    
    path('product/add/', views.manage_product, name='product_add'),
    path('product/edit/<int:pk>/', views.manage_product, name='product_edit'),
    path('category/add/', views.add_category, name='category_add'),
]