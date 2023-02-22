from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
from store.models import Product, Variations
from .models import Cart, CartItem


TAX_PERCATNAGE: int = 2


def _cart_id(request: HttpRequest) -> str:
    """
    Helper function to get the cart id from the session key, creating a new one if necessary

    Args:
        request: An instance of `HttpRequest`.

    Returns:
        A string representing the cart id.
    """
    cart = request.session.session_key

    if not cart:
        cart = request.session.create()

    return cart


def add_cart(request: HttpRequest, product_id: int) -> HttpResponseRedirect:
    """
    Adds a product to the cart or increases its quantity if it already exists in the cart

    Args:
        request: An instance of `HttpRequest`.
        product_id: An integer representing the id of the product to add to the cart.

    Returns:
        An instance of `HttpResponseRedirect` that redirects to the cart page.
    """
    product = Product.objects.get(id=product_id)
    product_variation = []

    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST.get(key)

            try:
                variation = Variations.objects.get(product=product, category__iexact=key, value__iexact=value)
                product_variation.append(variation)
            except Exception as e:
                print(e)

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )

    cart.save()

    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, cart=cart)

        ex_var_list = []
        id_list = []
        for item in cart_item:
            existing_variation = item.variation.all()
            ex_var_list.append(list(existing_variation))
            id_list.append(item.id)

        if product_variation in ex_var_list:
            # Increase the cart item quantity
            item_index = ex_var_list.index(product_variation)
            item_id = id_list[item_index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)

            if len(product_variation) > 0:
                item.variation.clear()
                item.variation.add(*product_variation)

            item.save()
    else:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart
        )

        if len(product_variation) > 0:
            cart_item.variation.clear()
            cart_item.variation.add(*product_variation)

        cart_item.save()

    return redirect('cart')


def remove_cart(request: HttpRequest, product_id: int, cart_item_id: int) -> HttpResponseRedirect:
    """
    Removes a quantity of a product from the cart or deletes it completely if the quantity is 1

    Args:
        request (HttpRequest): the HTTP request object
        product_id (int): the id of the product to remove from the cart
        cart_item_id (int): the id of the cart item to remove from the cart

    Returns:
        An instance of `HttpResponseRedirect` that redirects to the cart page.
    """
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)

    try:
        cart_item: CartItem = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass

    return redirect('cart')


def remove_cart_item(request: HttpRequest, product_id: int, cart_item_id: int) -> HttpResponseRedirect:
    """
    Remove a cart item from the cart.

    Args:
        request (HttpRequest): The HTTP request object.
        product_id (int): The ID of the product to remove.
        cart_item_id (int): The ID of the cart item to remove.

    Returns:
        An instance of `HttpResponseRedirect` that redirects to the cart page.
    """

    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()

    return redirect('cart')


def cart(request: HttpRequest, total: int = 0, quantity: int = 0, cart_items: list[CartItem] = None) -> HttpResponse:
    """
    Display the contents of the cart.

    Args:
        request (HttpRequest): The HTTP request object.
        total (int, optional): The total cost of the items in the cart. Defaults to 0.
        quantity (int, optional): The total quantity of items in the cart. Defaults to 0.
        cart_items (List[CartItem], optional): The list of cart items. Defaults to None.

    Returns:
        HttpResponse: The rendered cart page.
    """
    try:
        cart: Cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items: list[CartItem] = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity

        tax = Decimal(TAX_PERCATNAGE) / 100 * total
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': '%.2f'%tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)
