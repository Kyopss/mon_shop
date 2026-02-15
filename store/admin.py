from django.contrib import admin
from .models import Category, Product, ProductImage # <--- On importe le nouveau modèle

# Cette classe permet d'ajouter des images DANS la page du produit
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3 # On affiche 3 cases vides par défaut

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline] # <--- On active l'inline ici

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
# Pas besoin d'enregistrer ProductImage tout seul, il est dans Product maintenant