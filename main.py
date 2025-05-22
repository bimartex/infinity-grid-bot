import json, time
from grid_bot.api import BitgetAPI
from grid_bot.strategy import generate_grid
from grid_bot.logger import setup_logger

logger = setup_logger("GridBot")

with open('config.json') as f:
    config = json.load(f)

api = BitgetAPI(config)
symbol = config['symbol']
investment = config['investment']

while True:
    try:
        current_price = api.get_price(symbol)
        grid = generate_grid(current_price, config['grid_size'], config['price_range_percent'])

        grid_count = len(grid)
        amount_per_order = round(investment / grid_count, 4)
        qty = round(amount_per_order / current_price, 6)

        logger.info(f"Current price: {current_price}, Placing grid orders...")

        for price in grid:
            side = 'buy' if price < current_price else 'sell'
            logger.info(f"Placing {side} order at {price} for {qty}")
            resp = api.place_order(symbol, price, qty, side)
            logger.info(resp)
        
        time.sleep(30)  # Wait before repeating

    except Exception as e:
        logger.error(f"Error: {e}")
        time.sleep(60)  # Wait longer after an error
