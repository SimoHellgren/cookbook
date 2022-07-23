def test_get_all_when_empty(client):
    res = client.get("/recipes").json()
    assert len(res) == 0


def test_create(client):
    recipe = {
        "name": "Test recipe",
        "servings": 10,
        "method": "do the thing",
        "tags": "food",
    }

    res = client.post('/recipes/', json=recipe)

    assert res.status_code == 201

    data = res.json()

    assert data
    assert data["id"]
    assert recipe["name"] == data["name"]
    assert recipe["servings"] == data["servings"]
    assert recipe["method"] == data["method"]
    assert recipe["tags"] == data["tags"]
