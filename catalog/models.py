from os import name
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
import eav
from eav.registry import EavConfig, Attribute



class ItemStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'item status'

    def __str__(self):
        return self.name

class Category(MPTTModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name_plural = 'categories'
        unique_together = [('parent', 'slug')]

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    # def __str__(self):
    #     return self.name

    def __str__(self):
        ancestors = self.get_ancestors(include_self=True)
        return " / ".join(a.name for a in ancestors)

class Condition(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Variant(models.Model):
    parent = models.ForeignKey('CatalogItem', on_delete=models.CASCADE, related_name='conditions')
    sku = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=3, default=0.000)
    cost = models.DecimalField(max_digits=10, decimal_places=3, default=0.000)
    optimalQty = models.PositiveIntegerField(default=0)
    maxQty = models.PositiveIntegerField(default=0)
    qty = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
class ProductType(models.Model):
    name = models.CharField(max_length=100)
    attributes = models.ManyToManyField(eav.models.Attribute)
    conditions = models.ManyToManyField(Condition)

    def __str__(self):
        return self.name
    
class CatalogItem(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    barcode = models.CharField(max_length=100, unique=True, blank=True, null=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, related_name='items')
    description = models.TextField(blank=True, default='')
    image = models.ImageField(upload_to='catalog_images/', blank=True, null=True)
    online = models.BooleanField(default=True)
    status = models.ForeignKey(ItemStatus, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class CatalogItemConfig(EavConfig):

    def get_attributes(instance=None):
        try:
            pt = instance.product_type      
            return pt.attributes.all()
        except:
            return Attribute.objects.none()
    
eav.register(CatalogItem, CatalogItemConfig)