from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem

# On permet d'éditer les articles directement DANS la page de la commande
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"] # On ne peut pas tricher sur la date
    inlines = [OrderItemInline] # On affiche les articles liés

admin.site.register(ShippingAddress)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)