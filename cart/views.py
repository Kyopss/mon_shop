from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

def cart_summary(request):
    # 1. On récupère le panier
    cart = Cart(request)
    # 2. On récupère les vrais objets Produits (pour avoir le nom, l'image...)
    cart_products = cart.get_prods()
    # 3. On récupère les quantités (pour savoir combien de chaque)
    quantities = cart.get_quants()
    # 4. On récupère le total
    total = cart.get_total_price()

    return render(request, 'cart/cart_summary.html', { # Ajoute 'cart/' ici
    'cart_products': cart_products, 
    'quantities': quantities, 
    'total': total
    })

def cart_add(request):
    # On récupère le panier
    cart = Cart(request)

    # Si l'action est bien un "POST" (un clic sécurisé)
    if request.POST.get('action') == 'post':
        # 1. On récupère l'ID du produit envoyé par le bouton
        product_id = int(request.POST.get('product_id'))
        
        # 2. On cherche le produit dans la base de données
        product = get_object_or_404(Product, id=product_id)
        
        # 3. On l'ajoute au panier
        cart.add(product=product)

        # 4. On renvoie la nouvelle quantité totale au navigateur
        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity})
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        # On appelle la suppression dans le panier
        cart.delete(product=product_id)

        response = JsonResponse({'product': product_id})
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty': product_qty})
        return response