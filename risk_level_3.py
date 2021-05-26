# FOMO STRATEGY : Check on 1HR, entry on 1 minute
# AVOID FAKE OUT : Confirmation with 5 minute

import backtest
import config
import direction
import get_position
import HA_current
import place_order
import binance_futures_api
from datetime import datetime
from termcolor import colored

live_trade = config.live_trade

def lets_make_some_money(i):
    response = binance_futures_api.position_information(i)[0]
    mark_price   = binance_futures_api.mark_price(i)
    klines_1min  = binance_futures_api.KLINE_INTERVAL_1MINUTE(i)
    klines_5min  = binance_futures_api.KLINE_INTERVAL_5MINUTE(i)
    klines_30MIN = binance_futures_api.KLINE_INTERVAL_30MINUTE(i)
    klines_1HOUR = binance_futures_api.KLINE_INTERVAL_1HOUR(i)
    klines_6HOUR = binance_futures_api.KLINE_INTERVAL_6HOUR(i)
    position_info = get_position.get_position_info(i, response)
    profit = get_position.profit_threshold()

    if direction.clear_movement(klines_6HOUR): print(colored("CLEAR MOVEMENT   :   TRUE", "green"))
    else: print(colored("CLEAR MOVEMENT   :   FALSE", "red"))
    HA_current.output(mark_price, klines_1HOUR)
    HA_current.output(mark_price, klines_5min)
    HA_current.output(mark_price, klines_1min)
    
    leverage = int(config.leverage[i] + 10)
    if int(response.get("leverage")) != leverage: binance_futures_api.change_leverage(i, leverage)
    if response.get('marginType') != "isolated": binance_futures_api.change_margin_to_ISOLATED(i)
    if not live_trade: backtest.trigger_backtest(i, mark_price, profit, klines_1min)

    if position_info == "LONGING":
        if place_order.EXIT_LONG(response, mark_price, profit, klines_1min):
            if live_trade: binance_futures_api.close_position(i, "LONG")
            print("ACTION           :   💰 CLOSE_LONG 💰")

        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if place_order.EXIT_SHORT(response, mark_price, profit, klines_1min):
            if live_trade: binance_futures_api.close_position(i, "SHORT")
            print("ACTION           :   💰 CLOSE_SHORT 💰")

        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if direction.clear_movement(klines_6HOUR) and not direction.hot_zone(klines_30MIN, klines_6HOUR) and \
            place_order.GO_LONG(mark_price, klines_1min, klines_5min, klines_1HOUR):
            OPEN_LONG_POSITION(i, mark_price)

        elif direction.clear_movement(klines_6HOUR) and not direction.hot_zone(klines_30MIN, klines_6HOUR) and \
            place_order.GO_SHORT(mark_price, klines_1min, klines_5min, klines_1HOUR):
            OPEN_SHORT_POSITION(i, mark_price)

        else: DO_NOTHING(i)
    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

def OPEN_LONG_POSITION(i, mark_price):
    if live_trade:
        binance_futures_api.open_position(i, "LONG", config.quantity[i])
        print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
    else: backtest.demo_long(i, mark_price)

def OPEN_SHORT_POSITION(i, mark_price):
    if live_trade:
        binance_futures_api.open_position(i, "SHORT", config.quantity[i])
        print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
    else: backtest.demo_short(i, mark_price)

def DO_NOTHING(i):
    if live_trade: print("ACTION           :   🐺 WAIT 🐺")
    else:
        if backtest.retrieve_position(i) == "NONE":
            print("ACTION           :   🐺 WAIT 🐺")
