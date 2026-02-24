from decimal import Decimal
from django.conf import settings
from store.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, product, color):
        product_id = str(product.id)
        # Clé unique : ID_Couleur (ex: "4_Noir")
        selection_key = f"{product_id}_{color}"

        if selection_key in self.cart:
            self.cart[selection_key]['qty'] += 1
        else:
            self.cart[selection_key] = {
                'price': str(product.price),
                'qty': 1,
                'color': color,
                'product_id': product_id
            }

        self.session.modified = True

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def get_prods(self):
        # On extrait juste les IDs (le "4" de "4_Noir") pour chercher dans la DB
        product_ids = []
        for key in self.cart.keys():
            if '_' in str(key):
                product_ids.append(str(key).split('_')[0])
            else:
                product_ids.append(key)
        
        return Product.objects.filter(id__in=product_ids)

    def get_quants(self):
        return self.cart

    def cart_total(self):
        # On récupère les IDs pour chercher les produits dans la base de données
        product_ids = []
        for key in self.cart.keys():
            if '_' in str(key):
                product_ids.append(str(key).split('_')[0])
            else:
                product_ids.append(key)
        
        products = Product.objects.filter(id__in=product_ids)
        total = 0

        # Calcul du total simplifié (sans les soldes)
        for key, value in self.cart.items():
            key_id = str(value['product_id'])
            for product in products:
                if str(product.id) == key_id:
                    # On multiplie simplement le prix normal par la quantité
                    total += (product.price * value['qty'])
                    
        return total

    def delete(self, product_key):
        # Ici on attend la clé "4_Noir" directement
        if product_key in self.cart:
            del self.cart[product_key]
            self.session.modified = True
            
    def clear(self):
        self.session['session_key'] = {}
        self.session.modified = True
    
    def update(self, product_key, quantity):
        product_key = str(product_key)
        qty = int(quantity)

        # On met à jour la quantité du bon tiroir (ex: "4_Noir")
        if product_key in self.cart:
            self.cart[product_key]['qty'] = qty

        self.session.modified = True
        return self.cart