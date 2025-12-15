from django.shortcuts import render, redirect
from catalog.models import CatalogItem, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms
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

def register_user(request):
    form = SignUpForm
    if request.method=="POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #Login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("New account created! Welcome to Desert Rat Games"))
            return redirect('shop')
        else:
            messages.success(request, ("Bad news! Registration failed."))
            return redirect('register')
    else:
        return render(request, 'ecom/register.html', {'form':form, 'pageTitle': 'Register', 'pageSubtitle': 'Create a new account.'})
    
def product(request, pk):
    product = CatalogItem.objects.get(id=pk)
    attributes = product.eav.get_values_dict()
    # attributes = product.eav.get_all_attributes()
    return render(request, 'ecom/productDetail.html', {'product':product, 'attributes':attributes, 'pageTitle': 'none'})

def category(request, cat):
    try:
        category = Category.objects.get(slug=cat)
        print(category)
        products = category.items.all()
        print(products)
        return render(request, 'ecom/category.html', {'products':products, 'pageTitle':category.name, 'pageSubtitle': ''})
    except:
        messages.success(request, "That category doesn't exit.")
        return redirect('shop')
