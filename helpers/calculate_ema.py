# helpers/calculate_ema.py
"""
Calculate EMA module.
"""


# Funkcja obliczania EMA
def calculate_ema(series, period) -> float:
    """
    This function does something.

    Args:
        series: Description of param1.
        period: Description of param1.

    Returns:
        EMA value
    """
    return series.ewm(span=period, adjust=False).mean()
