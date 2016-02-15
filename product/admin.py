from django.contrib import admin
from django.core.urlresolvers import reverse
from product.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'created_at', 'modified_at')

    def view_on_site(self, obj):  # add view button to admin
        return reverse('product:product_view', kwargs={'slug': obj.slug})

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            # exclude field from edit fields
            kwargs['exclude'] = ['modified_at', ]
        return super(ProductAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(Product, ProductAdmin)
