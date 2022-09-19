from datetime import datetime
from backend.app.models import Recipe
from backend.tests.utils import create_random_recipe
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


def test_created_and_updated_timestamp(test_db):
    """Test that a created object gets a created timestamp"""
    obj = create_random_recipe(test_db)

    assert obj.created is not None
    assert obj.created < datetime.utcnow()

    assert obj.updated is not None
    assert obj.updated < datetime.utcnow()

    # created and updated should be equal
    assert obj.created == obj.updated


def test_updated_timestamp_updates(test_db):
    obj = create_random_recipe(test_db)

    before = datetime.utcnow()
    updated = obj.updated

    obj.name = "A name so long that there is no chance it already was this"
    test_db.add(obj)
    test_db.commit()
    test_db.refresh(obj)

    assert obj.updated > obj.created
    assert obj.updated > updated
    assert obj.updated > before
