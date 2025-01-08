# api/binance_client.py
"""
Binance client module.
"""

from decouple import config
from binance.client import Client

API_KEY = config('API_KEY')
API_SECRET = config('API_SECRET')
TESTNET = config('TESTNET')

# if TESTNET == 'True':
#     TESTNET = True
# else:
#     TESTNET = False
TESTNET = bool(TESTNET == 'True')

client = Client(API_KEY, API_SECRET, testnet=TESTNET)


if __name__ == '__main__':
    print(f"API_KEY: {API_KEY} | API_SECRET: {API_SECRET} | TESTNET: {TESTNET}")
