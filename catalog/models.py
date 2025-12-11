from os import name
from django.db import models
from autoslug import AutoSlugField
from mptt.models import MPTTModel, TreeForeignKey

class ItemStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'item status'

    def __str__(self):
        return self.name

class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Condition(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=3, default=0.000)
    cost = models.DecimalField(max_digits=10, decimal_places=3, default=0.000)
    optimalQty = models.PositiveIntegerField(default=0)
    maxQty = models.PositiveIntegerField(default=0)
    qty = models.PositiveIntegerField(default=0)
    item = models.ForeignKey('CatalogItem', on_delete=models.CASCADE, related_name='conditions')

    def __str__(self):
        return "Condition"
    
class CatalogItem(models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True)
    barcode = models.CharField(max_length=100, unique=True)
    category = models.ManyToManyField(Category, related_name='items')
    description = models.TextField(blank=True, default='')
    descriptor = models.JSONField(blank=True, null=True, default=dict)
    image = models.ImageField(upload_to='catalog_images/', blank=True, null=True)
    online = models.BooleanField(default=True)
    status = models.ForeignKey(ItemStatus, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title