from django.conf.urls import patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'product.views.products', name='products'),
    url(r'^products/(?P<slug>.+)/like/$', 'product.views.like', name='like'),
    url(r'^products/(?P<slug>.+)/$', 'product.views.product_view', name='product_view'),
                       )
