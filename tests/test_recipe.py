import os
import backend.db as db


def test_create_recipe():
    filename = "test_recipe.json"
    data = {
        "name": "test",
        "portions": 5,
        "ingredients": [{"name": "Test ingredient", "quantity": 1, "measure": "kpl"}],
        "method": "Put the thing in the place",
        "tags": ["tagge"]
    }
    db.create_recipe(filename=filename, **data)

    assert os.path.exists(f'./recipes/{filename}')

    os.remove(f'./recipes/{filename}')  # this leaves a file behind if the test fails
