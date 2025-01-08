# helpers/determine_trend.py
"""
Determine trend module.
"""


import pprint

from api.binance_client import client


def get_asset_balance(asset=None) -> dict:
    """
    This function does something.

    Args:
        asset: Description of param1.

    Returns:
        List of orders
    """
    try:
        assets = client.get_asset_balance(asset=asset)

        return assets

    except Exception as e:
        print(f"Błąd podczas pobierania zleceń: {e}")

    return {}


if __name__ == '__main__':
    pprint.pprint(get_asset_balance(asset='USDT'))
    pprint.pprint(get_asset_balance(asset='ETH'))
    pprint.pprint(get_asset_balance(asset='BTC'))
