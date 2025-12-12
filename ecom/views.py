from django.shortcuts import render
from catalog.models import CatalogItem


def shop(request):
    products = CatalogItem.objects.filter(online=True)
    return render(request, 'ecom/shop.html', {'pageTitle': 'Shop in style', 'pageSubtitle': 'With this shop homepage template', 'products': products})

def about(request):
    return render(request, 'ecom/about.html', {'pageTitle': 'About Us', 'pageSubtitle': 'Learn more about our company'})