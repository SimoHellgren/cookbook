from backend.app.models import Recipe


def test_as_dict():
    r = Recipe(
        name="Test recipe",
        servings=2.0,
        method="Do the thing with the ingredients",
        tags="japan,食べ物",
    )

    d = r.as_dict()

    expected_result = {
        "id": None,
        "name": "Test recipe",
        "servings": 2.0,
        "method": "Do the thing with the ingredients",
        "tags": "japan,食べ物",
    }

    assert d == expected_result
