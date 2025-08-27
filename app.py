import requests
import statistics
import time
import os
from datetime import datetime
from telegram import Bot

# --- Налаштування ---
TG_TOKEN = os.getenv("7759933501:AAF-DrVlX1I-wlWHGMOyXHM4rfoIhEX52sM")
TG_CHAT_ID = os.getenv("788305408")
bot = Bot(token=TG_TOKEN)

BYBIT_URL = "https://api.bybit.com/v5"

def get_klines(symbol, interval="5"):
    url = f"{BYBIT_URL}/market/kline?category=spot&symbol={symbol}&interval={interval}&limit=50"
    r = requests.get(url).json()
    if "result" not in r or "list" not in r["result"]:
        return []
    return r["result"]["list"]

def is_flat(symbol, threshold=0.3):
    klines = get_klines(symbol)
    if not klines:
        return False, 0
    highs = [float(k[2]) for k in klines]
    lows = [float(k[3]) for k in klines]
    rng = (max(highs) - min(lows)) / statistics.mean(highs) * 100
    return rng < threshold, rng

def main():
    url = f"{BYBIT_URL}/market/tickers?category=spot"
    data = requests.get(url).json()["result"]["list"]

    flat_list = []
    for coin in data:
        symbol = coin["symbol"]
        flat, rng = is_flat(symbol)
        if flat:
            flat_list.append(f"{symbol} у флеті ({rng:.2f}%)")

    if flat_list:
        msg = "📉 Монети у флеті:\n" + "\n".join(flat_list)
        bot.send_message(chat_id=TG_CHAT_ID, text=msg)
        print(msg)
    else:
        print("Флетів не знайдено", datetime.now())

if __name__ == "__main__":
    while True:
        main()
        time.sleep(300)
