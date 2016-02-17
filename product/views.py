import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
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
    # product = Product.objects.filter(slug__exact=slug)[0]
    product = get_object_or_404(Product, slug=slug)
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


@login_required
def like(request, slug):
    # import ipdb; ipdb.set_trace()
    if request.method == 'POST':
        user = request.user
        # slug = request.POST.get('slug', None)
        # product = Product.objects.filter(slug__exact=slug)[0]
        product = get_object_or_404(Product, slug=slug)

        if product.likes.filter(id=user.id).exists():
            # user has already liked this company
            # remove like/user
            product.likes.remove(user)
            message = 'You disliked this'
            messages.success(request, 'You disliked this')
        else:
            # add a new like for a company
            product.likes.add(user)
            message = 'You liked this'
            messages.success(request, 'You liked this')

    ctx = {'likes_count': product.total_likes, 'message': message}
    return HttpResponse(json.dumps(ctx), content_type='application/json')
