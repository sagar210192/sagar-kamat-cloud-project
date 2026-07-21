def register_and_login(client):
    client.post(
        "/auth/register",
        json={
            "email": "product@example.com",
            "password": "test123"
        }
    )

    client.post(
        "/auth/login",
        json={
            "email": "product@example.com",
            "password": "test123"
        }
    )


def test_get_products(client):
    response = client.get("/api/products")

    assert response.status_code == 200
    assert response.get_json() == []


def test_create_product_requires_login(client):
    response = client.post(
        "/api/products",
        json={
            "name": "Laptop",
            "price": 799.99,
            "stock": 5
        }
    )

    assert response.status_code == 401


def test_create_product(client):
    register_and_login(client)

    response = client.post(
        "/api/products",
        json={
            "name": "Laptop",
            "description": "Student laptop",
            "price": 799.99,
            "stock": 5
        }
    )

    assert response.status_code == 201
    assert response.get_json()["product"]["name"] == "Laptop"
