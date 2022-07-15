from decimal import Decimal, ROUND_HALF_UP


def float_to_decimal(x: float, decimals: int) -> Decimal:
    DECIMALS = Decimal(10) ** -decimals
    return Decimal(x).quantize(DECIMALS, rounding=ROUND_HALF_UP)
