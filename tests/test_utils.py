from backend.app.utils import float_to_decimal


def test_float_to_decimal():
    inp = 1.4
    _, digits, _ = float_to_decimal(inp, 1).as_tuple()

    assert digits == (1, 4)
