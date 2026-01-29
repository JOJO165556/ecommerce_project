from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db import transaction
from .models import Order, OrderItem, Product, Category
from .cart import Cart
from .forms import RegisterForm, ProductForm, CategoryForm

def is_admin(user):
    return user.is_staff

# Boutique & Auth
def product_list(request):
    # Simulation d'un bug critique qui paralyse tout le monolithe
    #1 / 0
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'shop/register.html', {'form': form})

# Gestion Panier
def cart_add(request, product_id):
    # 1. On bloque l'anonyme immédiatement
    if not request.user.is_authenticated:
        messages.error(request, "Veuillez vous connecter pour commencer vos achats.")
        return redirect('login')
    
    # 2. On bloque l'admin
    if request.user.is_staff:
        messages.error(request, "L'administrateur ne peut pas effectuer d'achats.")
        return redirect('home')
    
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    cart.add(product=product, quantity=quantity)
    messages.success(request, f"{product.name} ajouté au panier.")
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def cart_detail(request):
    if request.user.is_staff:
        return redirect('user_board')
    cart = Cart(request)
    return render(request, 'shop/cart_detail.html', {'cart': cart})

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

# Gestion Produit Admin
@user_passes_test(is_admin)
def manage_product(request, pk=None):
    product = get_object_or_404(Product, pk=pk) if pk else None
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Produit enregistré !")
            return redirect('home')
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/manage_product.html', {'form': form, 'edit_mode': pk is not None})

@user_passes_test(is_admin)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CategoryForm()
    return render(request, 'shop/manage_category.html', {'form': form})

# Commandes
@login_required
def user_board(request):
    orders = Order.objects.all().order_by('-created_at') if request.user.is_staff else Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/user_board.html', {'orders': orders})

@login_required
def update_order_status(request, order_id, new_status):
    if request.user.is_staff:
        order = get_object_or_404(Order, id=order_id)
        order.status = new_status
        order.save()
    return redirect('user_board')

def checkout(request):
    # 1. Vérification de la connexion avec message personnalisé
    if not request.user.is_authenticated:
        messages.error(request, "Veuillez vous connecter pour finaliser votre commande.")
        return redirect('login') 

    # 2. Sécurité pour l'admin
    if request.user.is_staff: 
        messages.warning(request, "Les administrateurs ne peuvent pas passer de commandes.")
        return redirect('home')
        
    cart = Cart(request)
    if len(cart) == 0: 
        messages.error(request, "Votre panier est vide.")
        return redirect('home')

    try:
        with transaction.atomic():
            order = Order.objects.create(user=request.user, total_price=cart.get_total_price())
            for item in cart:
                product = item['product']
                if product.stock < item['quantity']: 
                    raise Exception(f"Stock épuisé pour {product.name}")
                
                OrderItem.objects.create(
                    order=order, 
                    product=product, 
                    price=item['price'], 
                    quantity=item['quantity']
                )
                product.stock -= item['quantity']
                product.save()
            
            cart.clear()
            return render(request, 'shop/order_success.html', {'order': order})
            
    except Exception as e:
        messages.error(request, str(e))
        return redirect('cart_detail')