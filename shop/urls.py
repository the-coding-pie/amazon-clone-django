from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
  path('', views.home, name='home'),
  path('signup/', views.signup, name='signup'),
  path('signin/', views.signin, name='signin'),
  path('logout/', views.logout, name='logout'),
  path('product/<slug:slug>/', views.product_detail, name='detail'),
  path('category/<slug:slug>/', views.category, name='category'),
  path('search', views.search, name='search'),
  path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
  path('checkout_page/', views.checkout_page, name='checkout_page'),
]