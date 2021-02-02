clear_direction = False

import get_minute
import binance_futures
from datetime import datetime
from termcolor import colored
from get_hour import get_hour
from get_minute import emergency_minute
from get_position import get_position_info
from get_clear_direction import get_clear_direction

def scalping_no_trend():
    title = "ACTION           :   "
    position_info = get_position_info()
    five_minute   = get_minute.current_minute(5)
    one_minute    = get_minute.current_minute(1)

    if position_info == "LONGING": print(colored(title + "HOLDING_LONG", "green"))
    elif position_info == "SHORTING": print(colored(title + "HOLDING_SHORT", "red"))
    else:
        binance_futures.cancel_all_open_orders()
        if (one_minute == "GREEN") and ((five_minute == "GREEN") or (five_minute == "GREEN_INDECISIVE")):
            binance_futures.open_position("LONG")
            binance_futures.set_stop_loss("LONG")
            binance_futures.set_take_profit("LONG")
            print(colored(title + "🚀 GO_LONG 🚀", "green"))

        elif (one_minute == "RED") and ((five_minute == "RED") or (five_minute == "RED_INDECISIVE")):
            binance_futures.open_position("SHORT")
            binance_futures.set_stop_loss("SHORT")
            binance_futures.set_take_profit("SHORT")
            print(colored(title + "💥 GO_SHORT 💥", "red"))

        else: print(title + "🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

def scalping_with_trend():
    title = "ACTION           :   "
    position_info = get_position_info()
    if clear_direction: direction = get_clear_direction(4)
    else: direction = get_hour(6)
    five_minute   = get_minute.current_minute(5)
    one_minute    = get_minute.current_minute(1)

    if position_info == "LONGING": print(colored(title + "HOLDING_LONG", "green"))
    elif position_info == "SHORTING": print(colored(title + "HOLDING_SHORT", "red"))
    else:
        binance_futures.cancel_all_open_orders()
        if direction == "UP_TREND":
            if (one_minute == "GREEN") and ((five_minute == "GREEN") or (five_minute == "GREEN_INDECISIVE")):
                binance_futures.open_position("LONG")
                binance_futures.set_stop_loss("LONG")
                binance_futures.set_take_profit("LONG")
                print(colored(title + "🚀 GO_LONG 🚀", "green"))
            else: print("ACTION           :   🐺 WAIT 🐺")

        if direction == "DOWN_TREND":
            if (one_minute == "RED") and ((five_minute == "RED") or (five_minute == "RED_INDECISIVE")):
                binance_futures.open_position("SHORT")
                binance_futures.set_stop_loss("SHORT")
                binance_futures.set_take_profit("SHORT")
                print(colored(title + "💥 GO_SHORT 💥", "red"))
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print(title + "🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")