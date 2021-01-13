import os
import time
from datetime import datetime
from binance.client import Client

symbol   = "BTCUSDT"
quantity = 0.001

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

def get_timestamp():
    return int(time.time() * 1000)  

def get_current_trend():
    klines = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR, limit=3)

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), 2)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), 2)
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), 2)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), 2)

    current_Open    = round(((previous_Open + previous_Close) / 2), 2)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), 2)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)

    if (current_Open == current_High):
        print("Current TREND    :   🩸 DOWN Trend 🩸")
        trend = "DOWN_TREND"
    elif (current_Open == current_Low):
        print("Current TREND    :   🥦 UP Trend 🥦")
        trend = "UP_TREND"
    else:
        trend = "NO_TRADE_ZONE"
        if (current_Open > current_Close):
            print("Current TREND    :   😴 No Trade Zone おやすみ 🩸")
        elif (current_Close > current_Open):
            print("Current TREND    :   😴 No Trade Zone おやすみ 🥦")
        else:
            print("Current TREND    :   😴 No Color Zone おやすみ ( ͡° ͜ʖ ͡°)")
    return trend

def get_minute_candle():
    # The <limit> has to be 3x of the Interval Period
    klines = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=3)

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), 2)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), 2)
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), 2)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), 2)

    current_Open    = round(((previous_Open + previous_Close) / 2), 2)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), 2)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)

    if (current_Open == current_High):
        print("Current MINUTE   :   🩸 RED 🩸")
        minute_candle = "RED_CANDLE"
    elif (current_Open == current_Low):
        print("Current MINUTE   :   🥦 GREEN 🥦")
        minute_candle = "GREEN_CANDLE"
    else:
        if (current_Open > current_Close):
            print("Current MINUTE   :   RED_INDECISIVE 🩸")
            minute_candle = "RED_INDECISIVE"
        elif (current_Close > current_Open):
            print("Current MINUTE   :   GREEN_INDECISIVE 🥦")
            minute_candle = "GREEN_INDECISIVE"
        else:
            print("❗SOMETHING_IS_WRONG in get_minute_candle()❗")
            minute_candle = "SOMETHING_IS_WRONG"
    return minute_candle

def get_position_info():
    positionAmt = float(client.futures_position_information(symbol=symbol, timestamp=get_timestamp())[0].get('positionAmt'))
    if (positionAmt > 0):
        print("Current Position :   LONGING")
        return "LONGING"
    elif (positionAmt < 0):
        print("Current Position :   SHORTING")
        return "SHORTING"
    else:
        print("Current Position :   NO_POSITION")
        return "NO_POSITION"
          
def trade_action(position_info, trend, minute_candle):
    if position_info == "LONGING":
        if (minute_candle == "GREEN_CANDLE") or (minute_candle == "GREEN_INDECISIVE"):
            print("Action           :   WAIT 🐺")           # WAIT
        elif (minute_candle == "RED_CANDLE") or (minute_candle == "RED_INDECISIVE"):
            print("Action           :   CLOSE_LONG 😋")
            # CLOSE_LONG
            client.futures_create_order(symbol=symbol, side="SELL", type="MARKET", quantity=quantity, timestamp=get_timestamp())
        else:
            print("❗SOMETHING_IS_WRONG in trade_action()❗")

    elif position_info == "SHORTING":
        if (minute_candle == "GREEN_CANDLE") or (minute_candle == "GREEN_INDECISIVE"):
            print("Action           :   CLOSE_SHORT 😭")
            # CLOSE_SHORT
            client.futures_create_order(symbol=symbol, side="BUY", type="MARKET", quantity=quantity, timestamp=get_timestamp())
        elif (minute_candle == "RED_CANDLE") or (minute_candle == "RED_INDECISIVE"):
            print("Action           :   WAIT 🐺")           # WAIT
        else:
            print("❗SOMETHING_IS_WRONG in trade_action()❗")
            
    else:
        if trend == "UP_TREND":
            if (minute_candle == "GREEN_CANDLE"):
                print("Action           :   GO_LONG 🚀")
                client.futures_create_order(symbol=symbol, side="BUY", type="MARKET", quantity=quantity, timestamp=get_timestamp())
            else:
                print("Action           :   WAIT 🐺")       # WAIT
        elif trend == "DOWN_TREND":
            if (minute_candle == "RED_CANDLE"):
                print("Action           :   GO_SHORT 💥")
                client.futures_create_order(symbol=symbol, side="SELL", type="MARKET", quantity=quantity, timestamp=get_timestamp())
            else:
                print("Action           :   WAIT 🐺")       # WAIT
        else:
            print("Action           :   WAIT 🐺")           # WAIT

while True:
    # get_position_info() >>>   LONGING  //    SHORTING    // NO_POSITION
    # get_current_trend() >>>  UP_TREND  //   DOWN_TREND   // NO_TRADE_ZONE
    # get_minute_candle() >>> RED_CANDLE //  GREEN_CANDLE  // RED_INDECISIVE // GREEN_INDECISIVE // SOMETHING_IS_WRONG

    trade_action(get_position_info(), get_current_trend(), get_minute_candle())

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Last action executed by " + current_time + "\n")

    time.sleep(5)
