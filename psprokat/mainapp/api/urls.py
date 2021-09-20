from django.urls import path

from .api_views import (
    ProductAPIView,
    ProductDetailAPIView
)


urlpatterns = [
    path('products/', ProductAPIView.as_view(), name='products_list'),
    path('products/<str:id>/', ProductDetailAPIView.as_view(), name='products_detail')
]
