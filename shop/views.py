from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Product, Category
from django.views.generic import ListView
from django.urls import reverse
from .forms import SignupForm, SignInForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout as logout_user
from django.conf import settings
from cart.models import Cart, CartItem
from django.contrib.auth.decorators import login_required

def home(request):
  products = Product.objects.all()
  categories = Category.objects.all()
  return render(request, 'shop/index.html', {
    'products': products,
    'categories': categories
  })

def product_detail(request, slug):
  product = get_object_or_404(Product, slug=slug)
  categories = Category.objects.all()
  similar_items = Product.objects.filter(category=product.category).exclude(slug=slug)
  return render(request, 'shop/detail.html', {
    'product': product,
    'similar_items': similar_items,
    'categories': categories
  })

def category(request, slug):
  products = Product.objects.filter(category__slug=slug)
  categories = Category.objects.all()
  return render(request, 'shop/index.html', {
    'products': products,
    'name': slug,
    'categories': categories
  })

def search(request):
  query = request.GET.get('q')
  categories = Category.objects.all()
  if not query:
    return redirect('shop:home')
  
  # search in title, description, or features
  products = Product.objects.filter(category__name__icontains=query) | Product.objects.filter(name__icontains=query) | Product.objects.filter(description__icontains=query) | Product.objects.filter(features__icontains=query)

  return render(request, 'shop/index.html', {
    'products': products,
    'name': 'Search Results',
    'categories': categories
  })

def signup(request):
  if request.user.is_authenticated:
    return redirect("shop:home")
  if request.method == 'POST':
    form = SignupForm(request.POST)
    
    if form.is_valid():
      # create a new user
      form.save()

      messages.add_message(request, messages.SUCCESS, 'Your Account has been created successfully!')
      messages.add_message(request, messages.SUCCESS, 'Now Sign-In to continue...')
      return redirect("shop:signin")

  else:
    form = SignupForm()
  return render(request, 'auth/signup.html', {
    'form': form
  })

def signin(request):
  next_url = request.GET.get('next')

  if request.user.is_authenticated:
    return redirect("shop:home")
  if request.method == 'POST':
    form = SignInForm(request.POST)
    if form.is_valid():
      # check authentication
      email=form.cleaned_data.get('email')
      password=form.cleaned_data.get('password')
      if User.objects.filter(email=email):
        user = User.objects.filter(email=email)[0]
        # check password
        matched = check_password(password, user.password)
        if matched:
          # valid user
          # take cart from session and persist # it in db

          if not Cart.objects.filter(user=user):
            cart = Cart(user=user)
            cart.save()
          else:
            cart = Cart.objects.get(user=user)
            
          session_cart = request.session.get(settings.CART_SESSION_ID)

          if session_cart:
            for item_id, item in session_cart.items():
              product = Product.objects.get(id=int(item_id))

              if CartItem.objects.filter(product=product, cart=cart): 
                item_in_cart = CartItem.objects.filter(product=product, cart=cart)[0]
                # then the product already # exists
                # so increase the quantity
                item_in_cart.price = float(item['price'])
                item_in_cart.quantity += int(item['quantity'])
                item_in_cart.save()
              else:
                # if item is not present in the cart, then add it
                new_item = CartItem(product=product, price=float(item['price']), quantity=int(item['quantity']), cart=cart)
              
                new_item.save()

            # destroy all items from the session
            del request.session[settings.CART_SESSION_ID]
          # login
          login(request, user)
          messages.add_message(request, messages.SUCCESS, "Signed In successfully!")
          return redirect(next_url) if next_url else redirect("shop:home")
        else:
          messages.add_message(request, messages.ERROR, "Email or Password doesn't match!")
      else:
          messages.add_message(request, messages.ERROR, "Email or Password doesn't match!")
  else:
    form = SignInForm()
  return render(request, 'auth/signin.html', {
    'form': form
  })

def logout(request):
  logout_user(request)
  return redirect("shop:signin")

@login_required()
def shopping_cart(request):
  cart = Cart.objects.get(user=request.user)
  categories = Category.objects.all()
  products = CartItem.objects.filter(cart=cart)
  return render(request, "shop/shopping_cart.html", {
    "products": products,
    "name": "Shopping Cart",
    'categories':categories
  })

@login_required
def checkout_page(request):
  cart = Cart.objects.get(user=request.user)
  CartItem.objects.filter(cart=cart).delete()
  return render(request, "shop/checkout.html", {
    "name": "Checkout Page"
  })