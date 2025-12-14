from django.shortcuts import render, redirect
from catalog.models import CatalogItem
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def shop(request):
    products = CatalogItem.objects.filter(online=True)
    return render(request, 'ecom/shop.html', {'pageTitle': 'Shop in style', 'pageSubtitle': 'With this shop homepage template', 'products': products})

def about(request):
    return render(request, 'ecom/about.html', {'pageTitle': 'About Us', 'pageSubtitle': 'Learn more about our company'})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password'] 
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Login Successful!"))
            return redirect('shop')
        else:
            messages.success(request, ("Login failed, please try again..."))
            return redirect('login')
    else:        
        return render(request, 'ecom/login.html', {'pageTitle': 'Login', 'pageSubtitle': 'Login to your account.'})

def logout_user(request):
    logout(request)
    messages.success(request, ("You were successfully logged out."))
    return redirect('shop')