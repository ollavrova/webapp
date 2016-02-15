from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
                       
    url(r'^', include('product.urls', namespace="product")),

    url(r'^admin/', include(admin.site.urls)),
)
