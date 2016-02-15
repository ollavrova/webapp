from django.shortcuts import get_object_or_404, render
from .models import Product


def products(request):
    products = Product.objects.all()
    return render(request, 'product/index.html', {
        'products': products,
    })


def product_view(request, slug):
    # product = get_object_or_404(Product, slug=slug)
    product = Product.objects.filter(slug__exact=slug)[0]
    return render(request, 'product/product.html', {
        'product': product,
    })
