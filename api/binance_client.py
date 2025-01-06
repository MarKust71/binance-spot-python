from decouple import config
from binance.client import Client

API_KEY = config('API_KEY')
API_SECRET = config('API_SECRET')
TESTNET = config('TESTNET')

if TESTNET == 'True':
    TESTNET = True
else:
    TESTNET = False

# print(f"API_KEY: {API_KEY} | API_SECRET: {API_SECRET} | TESTNET: {TESTNET}")

client = Client(API_KEY, API_SECRET, testnet=TESTNET)
