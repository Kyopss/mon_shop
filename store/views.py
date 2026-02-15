from django.shortcuts import render, get_object_or_404
from .models import Product
from .models import Product, Category

def product_all(request):
    products = Product.objects.all() # Récupère tous les produits
    return render(request, 'store/home.html', {'products': products})

def product_detail(request, slug):
    # On cherche le produit qui a ce "slug"
    product = get_object_or_404(Product, slug=slug, is_available=True)
    return render(request, 'store/product_detail.html', {'product': product})

def category_list(request, category_slug):
    # On récupère la catégorie ou on affiche une erreur 404 si elle n'existe pas
    category = get_object_or_404(Category, slug=category_slug)
    # On filtre les produits par cette catégorie
    products = Product.objects.filter(category=category)
    
    return render(request, 'store/home.html', {
        'category': category,
        'products': products
    })