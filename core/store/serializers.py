from rest_framework import serializers
from .models import (
    Category, Product, ProductImage, Cart, CartItem,
    Order, OrderItem, ProductImageUpload, Review, Wishlist
)
from core.users.serializers import UserSerializer


# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model, supports nested categories.
    """
    # subcategories = serializers.PrimaryKeyRelatedField(
    #     many=True, read_only=True, help_text="List of subcategories."
    # )

    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


# Product Image Serializer
class ProductImageSerializer(serializers.ModelSerializer):
    """
    Serializer for the ProductImage model.
    """
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text']


class ProductImageUploadSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = ProductImageUpload
        fields = ["id", "image"]


class CreaeteProductImageUploadSerializer(serializers.Serializer):
    images = serializers.ListField(
        child=serializers.FileField(
            max_length=1000000,
            allow_empty_file=False,
            use_url=False
        ),
        write_only=True,
        allow_empty=False
    )


# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    Includes related images.
    """
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True,
        source='category'
    )
    images = ProductImageSerializer(many=True, read_only=True)
    image_urls = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        allow_empty=True,
        required=False
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'category', 'category_id',
            'stock', 'created_at', 'updated_at', 'images', 'image_urls'
        ]


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


# Cart Item Serializer
class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for CartItem model.
    Includes the related product details.
    """
    product = SimpleProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Product.objects.all(),
        source='product'
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'product_id']


# Cart Serializer
class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for Cart model.
    Includes related cart items.
    """
    items = CartItemSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'updated_at', 'items']


# Order Item Serializer
class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderItem model.
    Includes the related product details.
    """
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price']


# Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model.
    Includes related order items.
    """
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'total_amount', 'status',
            'created_at', 'updated_at', 'items'
        ]


# Review Serializer
class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review model.
    Includes user and product details.
    """
    # user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'comment', 'created_at']


# Wishlist Serializer
class WishlistSerializer(serializers.ModelSerializer):
    """
    Serializer for Wishlist model.
    Includes product details.
    """
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product', 'created_at']


