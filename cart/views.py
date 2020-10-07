from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from shop.models import Product
from .models import CartItem, Cart

# Create your views here.
def get_cart(request):
  # create a session with cart
  item_count = 0
  total = 0
  if request.user.is_authenticated:
    if Cart.objects.filter(user=request.user):
      cart = Cart.objects.filter(user=request.user)[0]
      items = CartItem.objects.filter(cart=cart)

      item_count = sum(item.quantity for item in items)
      total = sum(item.quantity * item.price for item in items)
  else:
    cart = request.session.get(settings.CART_SESSION_ID)

    if not cart:
      # create a new cart
      cart = request.session[settings.CART_SESSION_ID] = {}

    item_count = sum([product['quantity'] for product in cart.values()])
    total = sum([product['quantity'] * float(product['price']) for product in cart.values()])

  return JsonResponse({
    'status': 200,
    'item_count': item_count,
    'total': total,
  })

@require_http_methods(['POST'])
def add_to_cart(request):
  id = request.POST.get('id')
  item = Product.objects.get(id=id)

  if not item:
    return JsonResponse({
      'status': 404,
      'msg': 'Oops item not found'
    })

  item_id = str(item.id)

  product_quantity = 1
  item_stock = item.stock

  if request.user.is_authenticated:
    cart = Cart.objects.get(user=request.user)
    if cart:
      product = CartItem.objects.filter(product=item, cart=cart)
      if item.stock >= 1:
        if product:
          # if product is already present
          product = product[0]
          product.quantity += 1
          product.save()
          item.stock -= 1
          item.save()

          product_quantity = product.quantity
            
        else:
          # create a new product
          new_item = CartItem(product=item, price=float(item.price), quantity=1, cart=cart)
          new_item.save()
          item.stock -= 1
          item.save()
          product_quantity = 1
        item_stock = item.stock
  else:
    cart = request.session.get(settings.CART_SESSION_ID)

    if not cart:
      # create a new cart
      cart = request.session[settings.CART_SESSION_ID] = {}

    # check if item is already in the cart
    if item.stock >= 1:
      if item_id in cart.keys():
        # update the quantity
        cart[item_id]['quantity'] += 1
        item.stock -= 1
        item.save()

      else:
        # add as a new item
        cart[item_id] = {
          "quantity": 1,
          "price": str(item.price)
        }
        item.stock -= 1
        item.save()

      product_quantity = cart[item_id]['quantity']
      item_stock = item.stock

    # explicitly say session has been modified
    request.session.modified = True

  return JsonResponse({
    'status': 200,
    'msg': 'Item Added',
    'product_quantity': product_quantity,
    'item_stock': item_stock
  })

@require_http_methods(['POST'])
def remove_from_cart(request):
  id = request.POST.get('id')
  item = Product.objects.get(id=id)

  if not item:
    return JsonResponse({
      'status': 404,
      'msg': 'Oops item not found'
    })

  item_id = str(item.id)

  product_quantity = 1
  item_stock = item.stock

  if request.user.is_authenticated:
    cart = Cart.objects.get(user=request.user)
    if cart:
      product = CartItem.objects.filter(product=item, cart=cart)
      if product:
        # if product is already present
        product = product[0]
        if not (product.quantity - 1) < 1:
          product.quantity -= 1
          item.stock += 1
          item.save()
          product.save()

        product_quantity = product.quantity
        item_stock = item.stock
 
  return JsonResponse({
    'status': 200,
    'msg': 'Item Added',
    'product_quantity': product_quantity,
    'item_stock': item_stock
  })

@require_http_methods(['POST'])
def remove_cart(request):
  id = request.POST.get('id')
  item = Product.objects.get(id=id)
  
  if not item:
    return JsonResponse({
      'status': 404,
      'msg': 'Oops item not found'
    })

  item_id = str(item.id)

  if request.user.is_authenticated:
    cart = Cart.objects.get(user=request.user)
    if cart:
      product = CartItem.objects.filter(product=item, cart=cart)
      if product:
        product = product[0]
        # if product is already present
        # first refill the item.stock
        item.stock += product.quantity
        item.save()
        product.delete()
  return JsonResponse({
    'status': 200,
    'msg': 'Item Added'
  })