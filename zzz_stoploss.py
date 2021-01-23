live_trade = False
stop_loss = False
trailing_stop = False

import config
import time
import binance_futures
from termcolor import colored
def get_timestamp(): return int(time.time() * 1000)

def trade_action(position_info, trend, minute_candle):
    if position_info == "LONGING":
        if trend == "UP_TREND":
            if (minute_candle == "RED_CANDLE"):
                print("ACTION           :   💰 CLOSE_LONG 💰")
                if live_trade: binance_futures.close_position("LONG")
            else: print(colored("ACTION           :   ✊🥦 HOLDING_LONG 🥦💪", "green"))

        else: # HERE IS FOR STOP LOSS DOUBLE ORDER HANDLING
            if not (minute_candle == "GREEN_CANDLE") or not (minute_candle == "WEAK_GREEN"):
                print("ACTION           :   😭 CLOSE_LONG 😭")
                if live_trade: binance_futures.close_position("LONG")
            else: print(colored("ACTION           :   ✊🥦 HOLDING_LONG 🥦💪", "green"))

    elif position_info == "SHORTING":
        if trend == "DOWN_TREND":
            if (minute_candle == "GREEN_CANDLE"):
                print("ACTION           :   💰 CLOSE_SHORT 💰")
                if live_trade: binance_futures.close_position("SHORT")
            else: print(colored("ACTION           :   ✊🩸 HOLDING_SHORT 🩸💪", "red"))

        else: # HERE IS FOR STOP LOSS DOUBLE ORDER HANDLING
            if not (minute_candle == "RED_CANDLE") or not (minute_candle == "WEAK_RED"):
                print("ACTION           :   😭 CLOSE_LONG 😭")
                if live_trade: binance_futures.close_position("SHORT")
            else: print(colored("ACTION           :   ✊🩸 HOLDING_SHORT 🩸💪", "red"))

    else:
        binance_futures.cancel_all_open_orders()
        if trend == "UP_TREND":
            if (minute_candle == "GREEN_CANDLE"):
                print(colored("Action           :   🚀 GO_LONG 🚀", "green"))
                if live_trade:
                    binance_futures.open_position("LONG")
                    if trailing_stop: binance_futures.set_trailing_stop("LONG")
                    if stop_loss: binance_futures.set_stop_loss("LONG")
            else: print("ACTION           :   🐺 WAIT 🐺")

        elif trend == "DOWN_TREND":
            if (minute_candle == "RED_CANDLE"):
                print(colored("Action           :   💥 GO_SHORT 💥", "red"))
                if live_trade:
                    binance_futures.open_position("SHORT")
                    if trailing_stop: binance_futures.set_trailing_stop("SHORT")
                    if stop_loss: binance_futures.set_stop_loss("SHORT")
            else: print("ACTION           :   🐺 WAIT 🐺")

        elif trend == "COOLDOWN":
            print("ACTION           :   🐺 WAIT for COOLDOWN 🐺")

        else:
            print("ACTION           :   🐺 WAIT 🐺")
