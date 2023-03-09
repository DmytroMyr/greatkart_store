from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from django.core.paginator import Paginator, Page
from django.db.models import Q, QuerySet
from typing import Optional
from .models import Product, ReviewRating
from .forms import ReviewForm
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id


PRODUCTS_PER_PAGE: int = 10


def get_paged_product(request: HttpRequest, products: QuerySet) -> Page:
    """Get paged product list.

    Args:
        request (HttpRequest): HTTP request object.
        products (QuerySet): QuerySet object representing products.

    Returns:
        Page: Page object representing the current page of products.
    """
    paginator = Paginator(products, PRODUCTS_PER_PAGE)
    page = request.GET.get('page')
    return paginator.get_page(page)


def store(request: HttpRequest, category_slug: Optional[str] = None) -> HttpResponse:
    """View function for the store page.

    Args:
        request (HttpRequest): HTTP request object.
        category_slug (str, optional): Slug of the selected category. Defaults to None.

    Returns:
        HttpResponse: HTTP response object with rendered store page.
    """
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


def product_detail(request: HttpRequest, category_slug: str, product_slug: str) -> HttpResponse:
    """View function for the product detail page.

    Args:
        request (HttpRequest): HTTP request object.
        category_slug (str): Slug of the selected category.
        product_slug (str): Slug of the selected product.

    Returns:
        HttpResponse: HTTP response object with rendered product detail page.
    """
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
    """View function that handles a search request and returns a filtered list of products based on the provided keyword.

    Args:
        request (HttpRequest): HTTP request object.

    Returns:
        HttpResponse: HTTP response object with rendered search results page.
    """
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


def submit_review(request: HttpRequest, product_id: int) -> HttpResponse:
    """A view that handles submission of product reviews and ratings.

    Args:
        request (HttpRequest): The HTTP request object.
        product_id (int): The id of the product to review.

    Returns:
        HttpResponse: The HTTP response object.
    """
    url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)

            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                return redirect(url)

    return HttpResponse('Review sent')
