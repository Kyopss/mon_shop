from django.db import models

# 1. La table pour les catégories (Pulls, T-shirts...)
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True) # Le "slug" sert à faire une belle URL (ex: /pulls)

    def __str__(self):
        return self.name

# 2. La table pour les produits
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2) # ex: 9999.99
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# ... (Tes classes Category et Product sont au dessus)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/gallery/')

    def __str__(self):
        return f"Image pour {self.product.name}"

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    category = models.CharField(max_length=100, choices=[('color', 'Couleur'), ('size', 'Taille')])
    value = models.CharField(max_length=100) # ex: "Rouge", "Bleu"

    def __str__(self):
        return f"{self.product.name} - {self.category}: {self.value}"