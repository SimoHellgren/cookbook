from backend.app.models import Recipe
from decimal import Decimal


def test_as_dict() -> None:
    r = Recipe(
        name="Test recipe",
        servings=Decimal("2.0"),
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
        "source": None,
        "created": None,  # None because we don't commit
        "updated": None,  # None because we don't commit
    }

    assert d == expected_result
