import json
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.functions import Length
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Product, Comment
from django.template import RequestContext
from django.contrib import messages
from product.forms import CommentForm
from webapp.settings import PER_PAGE


from datetime import datetime, timedelta

today = datetime.now()
last_day = today - timedelta(hours=24)


def products(request):
    sort = request.GET.get('sort', None)
    if sort == 'like':
        # product_list = Product.objects.order_by(Length('likes').asc())
        product_list = Product.objects.order_by('like_amount')
    elif sort == '-like':
        # product_list = Product.objects.order_by(Length('likes').desc())
        product_list = Product.objects.order_by('-like_amount')
    else:
        product_list = Product.objects.all()
    paginator = Paginator(product_list, PER_PAGE)

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)
    return render(request, 'product/index.html', {
        'products': products,
    })


def product_view(request, slug):
    now = timezone.now()
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            try:
                comment.save()
                messages.success(request, 'Your comment added.')
            except Exception as e:
                messages.error(request, e.message)
    else:
        form = CommentForm()
    comment_list = Comment.objects.filter(product__id=product.id)\
        .filter(created_at__gte=last_day,created_at__lte=today)\
        .order_by('-created_at')
    return render(request, 'product/product.html',
                  {'product': product, 'now': now, 'form': form,
                   'comment_list': comment_list},
                  RequestContext(request))


@login_required
def like(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)
    context = dict()
    if request.method == 'POST':
        if product.likes.filter(id=user.id).exists():
            product.likes.remove(user)
            message = 'You disliked this'
            act = 'Like'
            messages.success(request, message)
        else:
            product.likes.add(user)
            message = 'You liked this'
            act = 'Dislike'
            messages.success(request, message)
        product.save()
        context['message'] = message
        context['act'] = act
    context['likes_count'] = product.total_likes
    return HttpResponse(json.dumps(context), content_type='application/json')
