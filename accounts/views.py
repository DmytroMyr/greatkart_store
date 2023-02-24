from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from .models import Account
from carts.models import Cart, CartItem
from carts.views import _cart_id
import requests


def registration_view(request: HttpRequest) -> HttpResponse:
    form = RegistrationForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        new_user = Account.objects.create_user(username, email, password)
        new_user.save()

        messages.success(request, 'You have been registred.')
        return redirect('login')
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/registration.html', context)


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)

        if user:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()

                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # getting the product variation by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variation.all()
                        product_variation.append(list(variation))

                    # getting the cart_items from the user to access his product variations
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id_list = []
                    for item in cart_item:
                        existing_variation = item.variation.all()
                        ex_var_list.append(list(existing_variation))
                        id_list.append(item.id)

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id_list[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except Exception as e:
                print(e)

            auth.login(request, user)
            url = request.META.get('HTTP_REFERER')
            try:
                query: str = requests.utils.urlparse(url).query
                params = dict(x.split("=") for x in query.split('&'))
                if 'next' in params:
                    next_page = params['next']
                else:
                    next_page = params['home']

                return redirect(next_page)
            except:
                return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials.')
            

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout_view(request: HttpRequest) -> HttpResponse:
    auth.logout(request)
    return redirect('/')


@login_required(login_url='login')
def dashboard_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'accounts/dashboard.html')
