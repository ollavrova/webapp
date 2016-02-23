import json
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView, View, CreateView, FormView
from .models import Product, Comment
from django.contrib import messages
from product.forms import CommentForm
from webapp.settings import PER_PAGE
from datetime import timedelta


VALID_SORTS = {
    "like": "like_amount",
    "unlike": "-like_amount",
}

DEFAULT_SORT = 'like'


class SortMixin(object):
    """
    View mixin which provides sorting for ListView.
    """
    default_sort_params = None

    def sort_queryset(self, qs, sort_by):
        return qs.order_by(sort_by)

    def get_default_sort_params(self):
        if self.default_sort_params is None:
            raise ImproperlyConfigured(
                "'SortMixin' requires the 'default_sort_params' attribute "
                "to be set.")
        return self.default_sort_params

    def get_sort_params(self):
        default_sort_by = self.get_default_sort_params()
        sort = self.request.GET.get('sort_by', default_sort_by)
        sort_by = VALID_SORTS.get(sort, VALID_SORTS[DEFAULT_SORT])
        return sort_by

    def get_queryset(self):
        return self.sort_queryset(
            super(SortMixin, self).get_queryset(),
            self.get_sort_params())

    def get_context_data(self, *args, **kwargs):
        context = super(SortMixin, self).get_context_data(*args, **kwargs)
        sort_by = self.get_sort_params()
        context['sort_by'] = sort_by
        return context


class ProductList(SortMixin, ListView):
    template_name = 'product/index.html'
    model = Product
    paginate_by = PER_PAGE
    default_sort_params = DEFAULT_SORT

    def get_context_data(self, *args, **kwargs):
        path = ''
        path += "%s" % "&".join(["%s=%s" % (key, value) for (key, value) in self.request.GET.items() if not key=='page'])
        context = super(ProductList, self).get_context_data(**kwargs)
        context['path'] = path
        return context


class ProductDetail(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        last_day = timezone.now() - timedelta(hours=24)
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['comment_list'] = Comment.objects.filter(product=self.object)\
                                                 .filter(created_at__gte=last_day)\
                                                 .order_by('-created_at')
        context['form'] = CommentForm(initial={'product': self.object})
        return context


class CommentAdd(CreateView):
    model = Comment
    form_class = CommentForm
    http_method_names = ['post']
    template_name = 'product/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CommentAdd, self).get_context_data(**kwargs)
        product = Product.objects.filter(slug=self.kwargs['slug']).first()
        context['product'] = product
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Your comment added.')
        return super(CommentAdd, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error!')
        return super(CommentAdd, self).form_invalid(form)

    def get_success_url(self):
        product = Product.objects.filter(slug=self.kwargs['slug']).first()
        return reverse('product:product_view', kwargs={'slug': product.slug})


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
