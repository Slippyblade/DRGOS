from django.urls import path
from . import views

urlpatterns = [
    # path('xxx', views.xxx, name='xxx')
    path('', views.shop, name='shop'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:cat>', views.category, name='category'),
]