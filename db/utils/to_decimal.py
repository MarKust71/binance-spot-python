"""
Converts a value to a Decimal object.
"""
from decimal import Decimal


def to_decimal(value) -> Decimal:
    """
    Converts a value to a Decimal object.
    :param value:
    :return:
    """
    if value is None:
        return Decimal(0)

    if isinstance(value, Decimal):
        return value

    return Decimal(str(value))
