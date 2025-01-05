from decouple import config
from binance.client import Client

from constants import TESTNET

API_KEY = config('API_KEY')
API_SECRET = config('API_SECRET')


client = Client(API_KEY, API_SECRET, testnet=TESTNET)
