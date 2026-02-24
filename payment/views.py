from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from cart.cart import Cart
from .forms import ShippingForm
from .models import ShippingAddress, Order, OrderItem
from store.models import Product

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    if request.user.is_authenticated:
        try:
            shipping_address = ShippingAddress.objects.get(user=request.user)
            form = ShippingForm(request.POST or None, instance=shipping_address)
        except ShippingAddress.DoesNotExist:
            form = ShippingForm(request.POST or None)

        if request.method == 'POST':
            if form.is_valid():
                shipping_address = form.save(commit=False)
                shipping_address.user = request.user
                shipping_address.save()
                return redirect('billing_info')
    else:
        form = ShippingForm(request.POST or None)

    return render(request, "payment/checkout.html", {
        "cart_products": cart_products,
        "quantities": quantities,
        "totals": totals,
        "form": form
    })

def billing_info(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    if request.user.is_authenticated:
        try:
            shipping_info = ShippingAddress.objects.get(user=request.user)
        except ShippingAddress.DoesNotExist:
            messages.success(request, "Veuillez d'abord remplir votre adresse.")
            return redirect('checkout')
    else:
        shipping_info = None

    return render(request, "payment/billing_info.html", {
        "cart_products": cart_products,
        "quantities": quantities,
        "totals": totals,
        "shipping_info": shipping_info,
    })

def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()

        # --- MOUCHARD 1 : Vérif des données ---
        print(f"👀 DEBUG - Panier complet: {cart.cart}")
        print(f"👀 DEBUG - Total calculé: {totals}")

        # Récupération de l'adresse
        try:
            shipping_address = ShippingAddress.objects.get(user=request.user)
            full_address = f"{shipping_address.address1}\n{shipping_address.city}, {shipping_address.zipcode}\n{shipping_address.state}"
            
            full_name = shipping_address.full_name
            email = shipping_address.email
        except:
            # Sécurité si pas d'adresse (cas rare)
            full_address = "Adresse inconnue"
            full_name = "Invité"
            email = "inconnu@email.com"

        # Création de la Commande
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            shipping_address=full_address,
            amount_paid=totals  # Ici on met le total qu'on a vu dans le debug
        )
        
        print(f"✅ Commande créée ID: {order.id} - Montant: {order.amount_paid}")

        # Création des Articles (Order Items)
        for product in cart_products:
            product_id = str(product.id)
            
            if product_id in quantities:
                # C'EST ICI QUE CA BLOQUAIT : On extrait la quantité du dictionnaire
                # On prend le dictionnaire complet {'price': '50.00', 'qty': 1}
                item_data = quantities[product_id]
                
                # On prend juste le chiffre 'qty'
                qty = int(item_data['qty'])
                
                price = product.price
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    user=request.user,
                    quantity=qty,
                    price=price
                )
                print(f"✅ Article ajouté: {product.name} (Qté: {qty})")
            else:
                print(f"❌ Article non trouvé dans quantities: {product_id}")

        # On vide le panier
        cart.clear()

        return JsonResponse({'success': True, 'order_id': order.id})
    
    return JsonResponse({'success': False})