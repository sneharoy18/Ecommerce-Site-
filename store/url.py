'''from django.urls import path
from store import views
from django.urls import re_path
urlpatterns = [
    re_path(r'^$', views.store, name='store'),
	re_path(r'cart/', views.cart,name='cart'),
	re_path(r'checkout/', views.checkout,name='checkout'),
	re_path(r'update_item/', views.updateItem,name='update_item'),
]'''
from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem,name='update_item'),
	path('process_order/', views.processOrder,name='process_order'),
	path('login/', views.userLogin,name='login'),
	path('register/', views.registerPage, name="register"),
	path('logout/', views.logoutUser, name="logout"),
	path('orders/', views.ordersHistory, name="orders"),
	path('product_views/<str:pk>/', views.viewProduct, name="product_views"),

]
