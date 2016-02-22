from django.conf.urls import patterns, url
from django.contrib import admin
from product.views import ProductList, ProductDetail, CommentAdd

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', ProductList.as_view(), name='products'),
    url(r'^products/(?P<slug>.+)/comment/$', CommentAdd.as_view(), name='comment_add'),
    url(r'^products/(?P<slug>.+)/like/$', 'product.views.like', name='like'),
    url(r'^products/(?P<slug>.+)/$', ProductDetail.as_view(), name='product_view'),
                       )
