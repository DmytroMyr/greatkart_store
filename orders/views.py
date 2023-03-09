from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from decimal import Decimal
import datetime
import json
from uuid import uuid4
from carts.models import CartItem
from carts.views import TAX_PERCATNAGE
from .forms import OrderForm
from .models import Order, Payment, OrderProduct
from store.models import Product


def payments(request: HttpRequest) -> HttpResponse:
    """Processes the payment for an order and saves the payment details and order details.

    Args:
        request (HttpRequest): The request object that contains metadata about the request.

    Returns:
        HttpResponse: The response object that contains the JSON data for order number and transaction ID.
    """
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    
    payment = Payment(
        user = request.user,
        payment_id = uuid4(),
        payment_method = body['paymentMethod'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart items to Order Product Table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        order_product = OrderProduct()
        order_product.order = order
        order_product.payment = payment
        order_product.user = request.user
        order_product.product_id = item.product_id
        order_product.quantity = item.quantity
        order_product.product_price = item.product.price
        order_product.ordered = True
        order_product.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variation.all()
        order_product = OrderProduct.objects.get(id=order_product.id)
        order_product.variation.set(product_variation)
        order_product.save()

        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # Clear the cart
    CartItem.objects.filter(user=request.user).delete()

    # Send order recieved email to customer
    # ...

    # Send order number and transaction id back to sendPaymentsData function via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,

    }
    return JsonResponse(data)


def place_order(request: HttpRequest, total: int = 0, quantity: int = 0) -> HttpResponseRedirect:
    """Places an order for items in the cart.

    Args:
        request (HttpRequest): The request object that contains metadata about the request.
        total (int, optional): The total cost of the order. Defaults to 0.
        quantity (int, optional): The total quantity of the order. Defaults to 0.

    Returns:
        HttpResponseRedirect: Redirects to the home page if the cart is empty, 
        otherwise returns a payments page if the order is successful,
        or the checkout page with form errors if the form is invalid.
    """
    cart_items = CartItem.objects.filter(user=request.user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('store')

    if request.method == 'POST':
        form = OrderForm(request.POST)

        grand_total = 0
        tax = 0

        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity

        tax = Decimal(TAX_PERCATNAGE) / 100 * total
        grand_total = total + tax

        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = request.user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.city = form.cleaned_data['city']
            data.address = form.cleaned_data['address']
            data.comment = form.cleaned_data['comment']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            mt = int(datetime.date.today().strftime('%m'))
            dt = int(datetime.date.today().strftime('%d'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime('%Y%m%d')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)

            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': '%.2f'%tax,
                'grand_total': '%.2f'%grand_total,
            }
            return render(request, 'orders/payments.html', context)
        else:
            errors = form.errors.as_data()

            context = {
                'errors': errors,
                'cart_items': cart_items,
                'total': total,
                'tax': '%.2f' % tax,
                'grand_total': '%.2f' % grand_total,
            }

            return render(request, 'store/checkout.html', context)
    else:
        return redirect('home')


def order_complete(request: HttpRequest):
    """Displays the order completion page after a successful payment transaction.

    Args:
        request (HttpRequest): The request object that contains metadata about the request.

    Returns:
        HttpResponse: The response object that contains the HTML page of the order completion with order and payment details.
        
    Raises:
        Payment.DoesNotExist: If payment transaction does not exist.
        Order.DoesNotExist: If order does not exist or has not been ordered.
    """
    
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        order_products = OrderProduct.objects.filter(order_id=order.id)

        payment = Payment.objects.get(payment_id=transID)

        sub_total = 0
        for item in order_products:
            sub_total += item.product_price * item.quantity

        context = {
            'order': order,
            'order_products': order_products,
            'order_number': order.order_number,
            'payment_id': payment.payment_id,
            'payment': payment,
            'sub_total': sub_total,
        }
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
