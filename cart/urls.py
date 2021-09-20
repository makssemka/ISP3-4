from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<str:slug>/', views.cart_add, name='cart_add'),
    path('remove/<str:slug>/', views.cart_remove, name='cart_remove'),
]
