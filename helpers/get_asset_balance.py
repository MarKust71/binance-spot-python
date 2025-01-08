import pprint

from api.binance_client import client
from constants import TRADE_SYMBOL


def get_asset_balance(asset=None):
    try:
        assets = client.get_asset_balance(asset=asset)

        return assets

    except Exception as e:
        print(f"Błąd podczas pobierania zleceń: {e}")

    return None


if __name__ == '__main__':
    pprint.pprint(get_asset_balance(asset='USDT'))
    pprint.pprint(get_asset_balance(asset='ETH'))
    pprint.pprint(get_asset_balance(asset='BTC'))
