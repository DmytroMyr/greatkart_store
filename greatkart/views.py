from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from store.models import Product


def home(request: HttpRequest) -> HttpResponse:
    """Render the home page with a list of available products.

    Args:
        request (HttpRequest): The HTTP request sent by the client.

    Returns:
        HttpResponse: The HTTP response containing the rendered home page.

    """
    products = Product.objects.filter(is_available=True)

    context = {
        'products': products
    }
    
    return render(request, 'home.html', context)