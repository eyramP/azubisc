from django.urls import path
from .views import (
    ProductCreateListView, ProductDetailView,
    CartView, CartItemView, CategoryView, UploadProductImagesView
)

urlpatterns = [
    # Product Endpoints ////////////////////
    path('categories/', CategoryView.as_view(), name='product-categories'),
    path('product_images/', UploadProductImagesView.as_view(), name='upload-prpduct-images'),
    path('products/', ProductCreateListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    # Cart Endpoints /////////////////////
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/<int:pk>/', CartItemView.as_view(), name='cart-items'),
    # path('cart/items/<int:pk>/', CartItemView.as_view(), name='cart-items'),
]
