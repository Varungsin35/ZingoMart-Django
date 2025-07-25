from django.shortcuts import render,redirect,get_object_or_404
from store.models import product
from .models import Cart , CartItem



# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request,product_id):
    products = product.objects.get(id=product_id)  # get the product
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))  # get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
        cart.save()
    try:
        cart_item = CartItem.objects.get(products=products,cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            products = products,
            quantity = 1,
            cart = cart
        )
        cart_item.save()
    return redirect('cart')

def remove_cart(request,product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    products = get_object_or_404(product,id=product_id)
    cart_item = CartItem.objects.get(products=products,cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_item(request,product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    products = get_object_or_404(product,id=product_id)
    cart_item = CartItem.objects.get(products=products,cart=cart)
    cart_item.delete()
    return redirect('cart')

def cart(request,total=0,quantity=0,cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.products.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except Exception as e:
        pass # just ignore
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
    }
    return render(request,'store/cart.html',context)
