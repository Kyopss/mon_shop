from .cart import Cart

# Créer un processeur de contexte pour que le panier soit dispo sur toutes les pages
def cart(request):
    return {'cart': Cart(request)}