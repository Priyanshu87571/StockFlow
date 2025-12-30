def test_create_product(client):
    response = client.post("/api/products", json={
        "name": "Test Product",
        "sku": "TEST-001",
        "price": "10.00"
    })
    assert response.status_code == 201
