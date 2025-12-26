from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect

from mptt.admin import DraggableMPTTAdmin
from eav.forms import BaseDynamicEntityForm
from eav.admin import BaseEntityAdmin

from .forms import NewProductForm
from .models import Category, CatalogItem, Variant, ItemStatus, ProductType, Condition

class ProductTypeAdmin(admin.ModelAdmin):
    filter_horizontal = [('attributes'),]
    filter_horizontal += [('conditions'),]

class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title','slug')
    prepopulated_fields = {'slug': ('name',)}


class VariantInline(admin.TabularInline):
    fields = ('name', 'sku', 'optimalQty', 'maxQty', 'price', 'cost', 'qty')
    model = Variant
    extra = 0
    classes = ['collapse']

class CatalogItemAdminForm(BaseDynamicEntityForm):
    model = CatalogItem

class CatalogItemAdmin(BaseEntityAdmin):
    list_display = ('title', 'barcode', 'product_type')
    list_filter = ('product_type',)
    search_fields = ('title', 'barcode')
    filter_horizontal = ('category',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [VariantInline]
    form = CatalogItemAdminForm

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [path('add-by-type/', self.admin_site.admin_view(self.add_by_type_view), name='add_by_type'),]
        return custom_urls + urls

    def add_by_type_view(self, request):
        if request.method == 'POST':
            form = NewProductForm(request.POST)
            if form.is_valid():
                typeID = form.cleaned_data['product_type'].id
                productName = form.cleaned_data['name']
                prod = CatalogItem.objects.create(title=productName, product_type_id=typeID)
                pt = ProductType.objects.get(id=typeID)

                #Create Variants based on Conditions associated with the ProductType
                for c in pt.conditions.all():
                    Variant.objects.create(name=c.name, parent=prod)

                return redirect(f'/admin/catalog/catalogitem/{prod.id}/change/')
        else:
            form = NewProductForm()

        context = self.admin_site.each_context(request)
        context['form'] = form
        context['title'] = 'Select Product Type'
        return render(request, 'catalog/createProduct.html', context)
    
    def add_view(self, request, form_url = "", extra_context=None):
        return redirect('admin:add_by_type')


admin.site.register(Category, CategoryAdmin)
admin.site.register(CatalogItem, CatalogItemAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Condition)
admin.site.register(ItemStatus)