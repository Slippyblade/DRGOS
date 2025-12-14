from django.shortcuts import render
from catalog.models import CatalogItem
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def shop(request):
    products = CatalogItem.objects.filter(online=True)
    return render(request, 'ecom/shop.html', {'pageTitle': 'Shop in style', 'pageSubtitle': 'With this shop homepage template', 'products': products})

def about(request):
    return render(request, 'ecom/about.html', {'pageTitle': 'About Us', 'pageSubtitle': 'Learn more about our company'})

def login_user(request):
    return render(request, 'ecom/login.html', {'pageTitle': 'Login', 'pageSubtitle': 'Login to your account.'})

def logout_user(request):
    pass