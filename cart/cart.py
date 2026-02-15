from decimal import Decimal
from django.conf import settings
from store.models import Product

class Cart():
    def __init__(self, request):
        """
        Initialise le panier.
        On vérifie si le client a déjà un panier dans sa session (cookie).
        S'il n'en a pas, on en crée un vide.
        """
        self.session = request.session
        cart = self.session.get('session_key')

        if 'session_key' not in self.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, product, color):
        product_id = str(product.id)
        # On crée une clé unique combinant ID et Couleur
        selection_key = f"{product_id}_{color}"

        if selection_key not in self.cart:
            self.cart[selection_key] = {
                'price': str(product.price),
                'qty': 1,
                'color': color, # On stocke la couleur
                'product_id': product_id
            }
        else:
            self.cart[selection_key]['qty'] += 1

    self.session.modified = True
        }
    else:
        self.cart[selection_key]['qty'] += 1

    self.session.modified = True

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_qty

        self.session.modified = True

    def __len__(self):
        """
        Compter les articles dans le panier (pour le petit badge '0' du menu)
        """
        return sum(item['qty'] for item in self.cart.values())

    def get_prods(self):
        """
        Récupérer les vrais objets Produits depuis la base de données
        pour les afficher dans le récapitulatif
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quants(self):
        """
        Récupérer juste les quantités (ex: {ID_produit: 2})
        """
        quantities = self.cart
        return quantities

    def get_total_price(self):
        """
        Calculer le prix total du panier (ex: 150.00 €)
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        total = 0

        for key, value in self.cart.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    total = total + (product.price * value['qty'])
        return total

    def delete(self, product):
        """
        Supprimer un produit
        """
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    def clear(self):
        # On vide le dictionnaire du panier
        self.session['session_key'] = {}
        self.session.modified = True