import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from ..models import Product, Cart, CartItem, Category


User = get_user_model()

@pytest.fixture
def admin_user():
    return User.objects.create_user(
        first_name="John",
        last_name='Doe',
        email='ecobblah2@gmail.com',
        password='pass5432',
        is_staff=True,
        is_superuser=True
    )

@pytest.fixture
def api_client():
    return APIClient()



@pytest.fixture
def user():
    return User.objects.create_user(
        first_name="John",
        last_name='Doe',
        email='cobblaheyram@yahoo.com',
        password="password"
    )


@pytest.fixture
def category():
    return Category.objects.create(
        id=1,
        name='Eletronics',
        description='Electronic products'
    )


@pytest.fixture
def product(category):
    return Product.objects.create(
        name="Test Product",
        description="Test Description",
        price=100.00,
        category_id=category.id,
        stock=3
    )


@pytest.fixture
def cart(user):
    return Cart.objects.create(user=user)


@pytest.fixture
def cart_item(cart, product):
    return CartItem.objects.create(cart=cart, product=product, quantity=1)