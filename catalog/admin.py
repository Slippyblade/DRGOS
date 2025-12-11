from django.contrib import admin
from .models import Category, CatalogItem, Condition, ItemStatus
from mptt.admin import DraggableMPTTAdmin


class CategoryAdmin(DraggableMPTTAdmin):
    # mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title',)
    # list_display_links = ('indented_title',)

class ConditionInline(admin.TabularInline):
    fields = ('name', 'sku', 'optimalQty', 'maxQty', 'price', 'cost', 'qty')
    model = Condition
    extra = 0

class CatalogItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'barcode')
    search_fields = ('title', 'barcode')
    filter_horizontal = ('category',)
    inlines = [ConditionInline]

admin.site.register(Category, CategoryAdmin)
admin.site.register(CatalogItem, CatalogItemAdmin)
admin.site.register(ItemStatus)