from django.contrib import admin
from .models import CartItem, Cart

# Register your models here.
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
  list_display = ['product', 'price', 'quantity', 'cart']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
  list_display = ['user']