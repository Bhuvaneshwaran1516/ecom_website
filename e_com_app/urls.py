"""
URL configuration for E_Com project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('home',views.home,name="home"),
    path('login',views.login , name="login"),
    path('logout',views.logout_page , name="logout"),   
    path('reg',views.reg, name="reg"),
    path('category',views.category,name="category"),
    path('category/<str:name>',views.categoryview , name="category"),
    path('category/<str:cname>/<str:pname>',views.product_details , name="product_details"),
    path('addtocart/<int:product_id>',views.addtocart,name="addtocart"),
    path('view_cart',views.view_cart, name="view_cart"),
    path('show_cart/<int:product_id>',views.show_cart, name="show_cart"),
    path('remove_cart/<int:product_id>',views.remove_cart, name="remove_cart"),
    path('favorites',views.view_favorites,name='view_favorites') ,
    path('show_favorites/<int:product_id>',views.show_favorites,name='show_favorites') ,
    path('add_to_favorites/<int:product_id>',views.add_to_favorites, name="add_to_favorites"),
    path('remove_from_favorites/<int:product_id>',views.remove_from_favorites, name="remove_from_favorites"),
    path('buy-now/<int:product_id>', views.buy_now, name='buy_now'),
    # path('order_detail/<int:order_id>', views.order_detail, name='order_detail'),
    path('orders', views.order_list, name='order_list'),
    path('search', views.search, name='search'),
    path('view_search/<int:product_id>',views.view_search, name="view_search"),
    path('add-shipping-address', views.add_shipping_address, name='add_shipping_address'),
    path('edit-shipping-address/<int:address_id>', views.edit_shipping_address, name='edit_shipping_address'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment_cancel/', views.payment_cancel, name='payment_cancel'),
    path('order_summary/<int:order_id>', views.order_summary, name='order_summary'),
    path('order_summary_pdf/<int:order_id>/', views.order_summary_pdf, name='order_summary_pdf'),


]


     


