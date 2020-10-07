from django.urls import path
from .import views

app_name = 'cart'

urlpatterns = [
  path('', views.get_cart, name='get_cart'),
  path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
  path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
  path('remove_cart/', views.remove_cart, name='remove_cart'),
]