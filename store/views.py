from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator, Page
from django.db.models import Q
from django.db.models.query import Q, QuerySet



PRODUCTS_PER_PAGE = 10

def get_paged_product(request: HttpRequest, products: QuerySet) -> Page:
    """Getting products per page"""

    paginator = Paginator(products, PRODUCTS_PER_PAGE)
    page = request.GET.get('page')
    return paginator.get_page(page)

def store(request: HttpRequest, category_slug: str = None) -> HttpResponse:
    categories = None
    products = None

    if category_slug:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(is_available=True, category=categories).order_by('id')
        product_count = products.count()
    else:
        products = Product.objects.filter(is_available=True).order_by('id')
        product_count = products.count()

    context = {
        'products': get_paged_product(request, products),
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }

    return render(request, 'store/product_detail.html', context)

def search(request: HttpRequest) -> HttpResponse:
    if 'keyword' in request.GET:
        keyword = request.GET.get('keyword').strip()

    products = Product.objects.filter(Q(description__icontains=keyword) | 
                                      Q(title__icontains=keyword) | 
                                      Q(category__title__icontains=keyword)).order_by('-created_date')
    product_count = products.count()

    context = {
        'products': get_paged_product(request, products),
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)
