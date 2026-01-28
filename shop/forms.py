from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Category

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username", "email"]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'price', 'stock', 'description', 'image_url']
        widgets = {
            'category': forms.Select(attrs={'class': 'w-full p-2 border rounded mb-4'}),
            'name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded mb-4'}),
            'price': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded mb-4'}),
            'stock': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded mb-4'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 border rounded mb-4', 'rows': 3}),
            'image_url': forms.URLInput(attrs={'class': 'w-full p-2 border rounded mb-4', 'placeholder': 'https://lien-image.com/photo.jpg'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded mb-4'}),
        }