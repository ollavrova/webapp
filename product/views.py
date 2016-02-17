from django.shortcuts import render
from django.utils import timezone
from .models import Product
from django.template import RequestContext
from django.contrib import messages
from product.forms import CommentForm


def products(request):
    products = Product.objects.all()
    return render(request, 'product/index.html', {
        'products': products,
    })


def product_view(request, slug):
    now = timezone.now()
    product = Product.objects.filter(slug__exact=slug)[0]
    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():  # and request.is_ajax():
            comment = form.save(commit=False)
            comment.product = product
            try:
                comment.save()
                messages.success(request, 'Your comment added.')
            except Exception as e:
                messages.error(request, e.message)
    else:
        form = CommentForm()
    return render(request, 'product/product.html',
                  {'product': product, 'now': now, 'form': form},
                  RequestContext(request))


