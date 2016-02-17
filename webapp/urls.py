from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^', include('product.urls', namespace="product")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'registration/login.html'},
        name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout'),
)
