from django.urls import path
from .views import (
    ProductCreateListView, ProductDetailView,
    CartView, CartItemView, CategoryVIEW
)

urlpatterns = [
    # Product Endpoints ////////////////////
    path('categories/', CategoryVIEW.as_view(), name='product-categories'),
    path('products/', ProductCreateListView.as_view(), name='product-list'),
    path('details/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    # Cart Endpoints /////////////////////
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/<int:pk>/', CartItemView.as_view(), name='cart-item'),
]
