from django.db import models
from django.contrib.auth.models import User
from shop.models import Product

class Cart(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')

  def __str__(self):
    return f"Cart of ${self.user.username}"

class CartItem(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  quantity = models.IntegerField(default=0)
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')

  def __str__(self):
    return self.product.name
