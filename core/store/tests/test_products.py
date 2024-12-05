import pytest

from core.store.models import CartItem


@pytest.mark.django_db
def test_get_all_products(api_client, product):
    response = api_client.get("http://localhost:9090/api/v1/store/products/")
    assert response.status_code == 200
    assert len(response.data) > 0


@pytest.mark.django_db
def test_get_product_by_id(api_client, product):
    response = api_client.get(f"http://localhost:9090/api/v1/store/products/{product.id}/")
    assert response.status_code == 200
    assert response.data["name"] == product.name


@pytest.mark.django_db
def test_add_product(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    data = {
        "name": "New Product",
        "description": "A new product description",
        "price": 150.00,
        "stock": 1,
        "category": 1,
        "images": ["products/images/df5d4a72-ef8f-4143-af81-2dab3c287228.957e3a3a8cce28d1a6a5d6ebf4df097f_XZdBOX8.jpeg"]
    }
    response = api_client.post("http://localhost:9090/api/v1/store/products/", data)
    assert response.status_code == 201
    assert response.data["name"] == data["name"]


@pytest.mark.django_db
def test_update_product(api_client, admin_user, product):
    api_client.force_authenticate(user=admin_user)
    data = {"name": "Updated Product"}
    response = api_client.put(f"http://localhost:9090/api/v1/store/products/{product.id}/", data)
    assert response.status_code == 200
    assert response.data["name"] == "Updated Product"


@pytest.mark.django_db
def test_delete_product(api_client, admin_user, product):
    api_client.force_authenticate(user=admin_user)
    response = api_client.delete(f"http://localhost:9090/api/v1/store/products/{product.id}/")
    assert response.status_code == 204


@pytest.mark.django_db
def test_get_cart(api_client, user, cart, cart_item):
    api_client.force_authenticate(user=user)
    response = api_client.get("http://localhost:9090/api/v1/store/cart/")
    assert response.status_code == 200
    assert len(response.data["cart_items"]) == 0


@pytest.mark.django_db
def test_add_to_cart(api_client, user, product):
    api_client.force_authenticate(user=user)
    data = {
         "products":
            {"product": 1, "quantity": 3}
    }

    response = api_client.post("http://localhost:9090/api/v1/store/cart/", data)
    assert response.status_code == 201
    assert response.data["cart_items"][0]["product"]["id"] == product.id
    assert response.data["cart_items"][0]["quantity"] == 2


@pytest.mark.django_db
def test_update_cart_item(api_client, user, cart_item):
    api_client.force_authenticate(user=user)
    data = {"quantity": 5}
    response = api_client.put(f"http://localhost:9090/api/v1/store/cart/{cart_item.id}/", data)
    assert response.status_code == 200
    assert response.data["quantity"] == 5


@pytest.mark.django_db
def test_remove_cart_item(api_client, user, cart_item):
    api_client.force_authenticate(user=user)
    response = api_client.delete(f"http://localhost:9090/api/v1/store/cart/{cart_item.id}/")
    assert response.status_code == 204

    assert not CartItem.objects.filter(id=cart_item.id).exists()