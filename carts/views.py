from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from decimal import Decimal
from store.models import Product
from .models import Cart, CartItem


TAX_PERCATNAGE = 2

def _cart_id(request: HttpRequest) -> HttpResponse:
    cart = request.session.session_key

    if not cart:
        cart = request.session.create()

    return cart

def add_cart(request: HttpRequest, product_id: int) -> HttpResponseRedirect:
    """Adding a product to the cart"""

    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )

    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart
        )
        cart_item.save()

    return redirect('cart')

def remove_cart(request: HttpRequest, product_id: int) -> HttpResponseRedirect:
    """Decrising the quantity of the product or delete it"""

    cart: Cart = Cart.objects.get(cart_id=_cart_id(request))
    product: Product = get_object_or_404(Product, id=product_id)
    cart_item: CartItem = CartItem.objects.get(product=product, cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

def remove_cart_item(request: HttpRequest, product_id: int) -> HttpResponseRedirect:
    """Removing the item from the cart"""

    cart: Cart = Cart.objects.get(cart_id=_cart_id(request))
    product: Product = get_object_or_404(Product, id=product_id)
    cart_item: CartItem = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()

    return redirect('cart')

def cart(request: HttpRequest, total: int = 0, quantity: int = 0, cart_items: CartItem = None) -> HttpResponse:
    try:
        cart: Cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items: list[CartItem] = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity

        tax = Decimal(TAX_PERCATNAGE) / 100 * total
        grand_total = total + tax
    except ObjectNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)
