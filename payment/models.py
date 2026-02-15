from django.db import models
from django.contrib.auth.models import User
from store.models import Product

# 1. L'Adresse de livraison
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    address1 = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, null=True, blank=True) # Région/Pays
    zipcode = models.CharField(max_length=20, null=True, blank=True)
    
    # Pour l'admin : afficher le nom proprement
    class Meta:
        verbose_name_plural = "Shipping Addresses"

    def __str__(self):
        return f'Adresse de - {str(self.id)}'

# 2. La Commande globale (Le ticket de caisse)
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    shipping_address = models.TextField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Commande - {str(self.id)}'

# 3. Les Articles dans la commande (Ligne par ligne)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Order Item - {str(self.id)}'