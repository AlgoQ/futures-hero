import config
import heikin_ashi
import get_position
import binance_futures
from datetime import datetime
from termcolor import colored

def dead_or_alive():
    position_info = get_position.get_position_info()
    direction    = heikin_ashi.get_hour(6)
    one_hour     = heikin_ashi.get_hour(1)
    five_minute  = heikin_ashi.get_current_minute(5)
    one_minute   = heikin_ashi.get_current_minute(1)

    if position_info == "LONGING":
        if DIRECTION_CHANGE_EXIT_LONG(one_hour) or ((get_position.get_unRealizedProfit() == "PROFIT") and CLOSE_LONG()):
            print("ACTION           :   💰 CLOSE_LONG 💰")
            binance_futures.close_position("LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if DIRECTION_CHANGE_EXIT_SHORT(one_hour) or ((get_position.get_unRealizedProfit() == "PROFIT") and CLOSE_SHORT()):
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            binance_futures.close_position("SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        previous_volume = binance_futures.get_volume("PREVIOUS", "1HOUR")
        current_volume = binance_futures.get_volume("CURRENT", "1HOUR")

        if direction == "GREEN" and volume_confirmation(previous_volume, current_volume):
            if GO_LONG(one_minute, five_minute, one_hour):
                print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
                if config.live_trade: binance_futures.open_position("LONG", trade_amount())
            else: print("ACTION           :   🐺 WAIT 🐺")

        elif direction == "RED" and volume_confirmation(previous_volume, current_volume):
            if GO_SHORT(one_minute, five_minute, one_hour):
                print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
                if config.live_trade: binance_futures.open_position("SHORT", trade_amount())
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

def fomo_strifing():
    position_info = get_position.get_position_info()
    one_hour     = heikin_ashi.get_hour(1)
    five_minute  = heikin_ashi.get_current_minute(5)
    one_minute   = heikin_ashi.get_current_minute(1)

    if position_info == "LONGING":
        if DIRECTION_CHANGE_EXIT_LONG(one_hour) or ((get_position.get_unRealizedProfit() == "PROFIT") and CLOSE_LONG()):
            print("ACTION           :   💰 CLOSE_LONG 💰")
            binance_futures.close_position("LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if DIRECTION_CHANGE_EXIT_SHORT(one_hour) or ((get_position.get_unRealizedProfit() == "PROFIT") and CLOSE_SHORT()):
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            binance_futures.close_position("SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        previous_volume = binance_futures.get_volume("PREVIOUS", "1HOUR")
        current_volume = binance_futures.get_volume("CURRENT", "1HOUR")

        if one_hour == "GREEN" and volume_confirmation(previous_volume, current_volume):
            if GO_LONG(one_minute, five_minute, one_hour):
                print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
                if config.live_trade: binance_futures.open_position("LONG", config.quantity)
            else: print("ACTION           :   🐺 WAIT 🐺")

        elif one_hour == "RED" and volume_confirmation(previous_volume, current_volume):
            if GO_SHORT(one_minute, five_minute, one_hour):
                print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
                if config.live_trade: binance_futures.open_position("SHORT", config.quantity)
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print("ACTION           :   🐺 WAIT 🐺")
    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

from heikin_ashi import current_candle
from heikin_ashi import previous_candle
from heikin_ashi import pattern_broken
from heikin_ashi import pencil_wick_test
from heikin_ashi import one_minute_exit_test

def GO_LONG(one_minute, five_minute, one_hour):
    if ((pattern_broken("5MINUTE") == "NOT_BROKEN") and (pattern_broken("1HOUR") == "NOT_BROKEN")) and \
       ((one_minute == "GREEN") and (pencil_wick_test("GREEN", "1MINUTE") == "PASS")) and \
       (((five_minute == "GREEN") or (five_minute == "GREEN_INDECISIVE")) and (pencil_wick_test("GREEN", "5MINUTE") == "PASS")) and \
       ((one_hour == "GREEN" or one_hour == "GREEN_INDECISIVE") and (pencil_wick_test("RED", "1HOUR") == "FAIL")): return True

def GO_SHORT(one_minute, five_minute, one_hour):
    if ((pattern_broken("5MINUTE") == "NOT_BROKEN") and (pattern_broken("1HOUR") == "NOT_BROKEN")) and \
       ((one_minute == "RED") and (pencil_wick_test("RED", "1MINUTE") == "PASS")) and \
       (((five_minute == "RED") or (five_minute == "RED_INDECISIVE")) and (pencil_wick_test("RED", "5MINUTE") == "PASS")) and \
       (((one_hour == "RED") or (one_hour == "RED_INDECISIVE")) and (pencil_wick_test("GREEN", "1HOUR") == "FAIL")): return True

def CLOSE_LONG():
    if (one_minute_exit_test("GREEN")): return True

def CLOSE_SHORT():
    if (one_minute_exit_test("RED")): return True

def DIRECTION_CHANGE_EXIT_LONG(one_hour):
    if ((one_hour == "RED") and (pencil_wick_test("RED", "1HOUR") == "PASS")): return True

def DIRECTION_CHANGE_EXIT_SHORT(one_hour):
    if ((one_hour == "GREEN") and (pencil_wick_test("GREEN", "1HOUR") == "PASS")): return True

def volume_confirmation(previous_volume, current_volume):
    return current_volume > (previous_volume / 5)

def trade_amount():
    firstrun_volume = binance_futures.get_volume("FIRSTRUN", "6HOUR")
    previous_volume = binance_futures.get_volume("PREVIOUS", "6HOUR")
    current_volume  = binance_futures.get_volume("CURRENT", "6HOUR")

    if   (firstrun_volume < previous_volume) and (previous_volume < current_volume): trade_amount = config.quantity * 3
    elif (firstrun_volume > previous_volume) and (previous_volume > current_volume): trade_amount = config.quantity * 1
    else:
        if current_volume > previous_volume: trade_amount = config.quantity * 2
        else: trade_amount = config.quantity * 1

    return trade_amount
    # return config.quantity
