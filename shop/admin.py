from django.contrib import admin
from .models import Product, Category, Order, OrderItem

# 1. Enregistrement simple pour Category
admin.site.register(Category)

# 2. Enregistrement avec décorateur pour Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category')
    list_editable = ('price', 'stock')

# 3. Configuration de l'Inline pour les articles de commande
class OrderItemInline(admin.TabularInline): 
    model = OrderItem
    raw_id_fields = ['product'] 
    extra = 0

# 4. Enregistrement avec décorateur pour Order
@admin.register(Order)  # <--- C'est ici que l'enregistrement se fait !
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'status', 'created_at', 'updated_at']
    list_editable = ['status']
    list_filter = ['status', 'created_at']
    inlines = [OrderItemInline]
    readonly_fields = ['created_at', 'updated_at'] 