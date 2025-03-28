"""
Moduł zawierający funkcję obliczającą zysk z transakcji.
"""
def calculate_profit(
        quantity: float,
        price: float,
        trade_price: float,
        factor
) -> float:
    """Oblicza zysk z transakcji."""
    return round(quantity * (price - trade_price) * factor, 2)
