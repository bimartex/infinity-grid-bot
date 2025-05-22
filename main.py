import json
from grid_bot.api import BitgetAPI
from grid_bot.strategy import generate_grid

with open('config.json') as f:
    config = json.load(f)

api = BitgetAPI(config)
symbol = config['symbol']
investment = config['investment']

current_price = api.get_price(symbol)
grid = generate_grid(current_price, config['grid_size'], config['price_range_percent'])

# Calculate investment per level
grid_count = len(grid)
amount_per_order = round(investment / grid_count, 4)
qty = round(amount_per_order / current_price, 6)

for price in grid:
    side = 'buy' if price < current_price else 'sell'
    print(f"Placing {side} order at {price} for {qty} {symbol}")
    resp = api.place_order(symbol, price, qty, side)
    print(resp)
