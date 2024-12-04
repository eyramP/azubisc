from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


# Category Model /////////////////////
class Category(models.Model):
    """
    Represents product categories. Supports hierarchical categories with self-referencing.
    """
    name = models.CharField(verbose_name=_('category name'), max_length=100, help_text="Name of the category.")
    description = models.TextField(blank=True, null=True, help_text="Description of the category.")
    parent_category = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories',
        help_text="Parent category for nested categories."
    )

    def __str__(self):
        return self.name


# Product Model ///////////////////
class Product(models.Model):
    """
    Represents a product in the store.
    Links to a category and tracks stock, price, and timestamps.
    """
    name = models.CharField(max_length=255, help_text="Name of the product.")
    description = models.TextField(help_text="Detailed description of the product.")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price of the product.")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products", help_text="Category of the product."
    )
    stock = models.PositiveIntegerField(help_text="Number of items in stock.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the product was added.")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the product was last updated.")

    def __str__(self):
        return self.name


# Product Image Model /////////////////
class ProductImage(models.Model):
    """
    Links multiple images to a product with optional alt text for accessibility.
    """
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images", help_text="The product this image belongs to."
    )
    image = models.ImageField(upload_to="product_images/", help_text="Image file of the product.")
    alt_text = models.CharField(
        max_length=255, blank=True, help_text="Alternate text for the image (for accessibility)."
    )

    def __str__(self):
        return f"Image for {self.product.name}"


# Cart Model ///////////////////////
class Cart(models.Model):
    """
    Represents a user's shopping cart, which holds multiple cart items.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="cart", help_text="Owner of the cart."
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the cart was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the cart was last updated.")

    def __str__(self):
        return f"Cart for {self.user.username}"


# Cart Item Model ///////////////////////////////////
class CartItem(models.Model):
    """
    Represents individual items in a user's cart.
    """
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="items", help_text="The cart this item belongs to."
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, help_text="The product added to the cart.")
    quantity = models.PositiveIntegerField(default=1, help_text="Quantity of the product in the cart.")

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart {self.cart.id}"


# Order Model /////////////////////////////////
class Order(models.Model):
    """
    Represents an order placed by a user. Tracks status, total amount, and timestamps.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders", help_text="The user who placed the order."
    )
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Total amount for the order."
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending', help_text="Current status of the order."
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the order was placed.")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the order was last updated.")

    def __str__(self):
        return f"Order {self.id} for {self.user.username}"


# Order Item Model ///////////////////////////////////
class OrderItem(models.Model):
    """
    Represents individual products in an order.
    """
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items", help_text="The order this item belongs to."
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, help_text="The product ordered.")
    quantity = models.PositiveIntegerField(help_text="Quantity of the product ordered.")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Price of the product at the time of order."
    )

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in order {self.order.id}"


# Review Model
class Review(models.Model):
    """
    Allows users to rate and review products.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews", help_text="User who wrote the review."
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews", help_text="Product being reviewed."
    )
    rating = models.PositiveIntegerField(help_text="Rating given to the product.")
    comment = models.TextField(blank=True, null=True, help_text="Optional review comment.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the review was created.")

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"


# Wishlist Model
class Wishlist(models.Model):
    """
    Allows users to save products for later purchase.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="wishlist", help_text="The user who owns this wishlist."
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="wishlisted_by", help_text="The product in the wishlist."
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the product was added to the wishlist.")

    def __str__(self):
        return f"{self.product.name} in {self.user.username}'s wishlist"