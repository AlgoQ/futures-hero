import os
import sys
import time
import json
from binance.client import Client

# start = time.time()
# print(f"{time.time() - start} seconds\n")

symbol  = "ETHUSDT"
core    =  500

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

while True:
    price = client.get_symbol_ticker(symbol=symbol)
    print(list(list(price.items())[1]))
    time.sleep(1)