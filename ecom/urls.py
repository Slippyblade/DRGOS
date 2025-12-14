from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('xxx', views.xxx, name='xxx')
    path('', views.shop, name='shop'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout')


]
