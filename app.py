from pybit.unified_trading import HTTP
import pandas as pd
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = "7759933501:AAF-DrVlX1I-wlWHGMOyXHM4rfoIhEX52sM"
CHAT_ID = "788305408"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
BYBIT_URL = "https://api.bybit.com/v5"


def fetch_ohlcv(symbol, interval="60"):
    kline = client.get_kline(symbol=symbol, interval=interval, limit=200)['result']
    df = pd.DataFrame(kline)
    df['close'] = df['close'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['hl'] = df['high'] - df['low']
    df['hc'] = (df['high'] - df['close'].shift()).abs()
    df['lc'] = (df['low'] - df['close'].shift()).abs()
    df['tr'] = df[['hl','hc','lc']].max(axis=1)
    df['ATR'] = df['tr'].rolling(14).mean()
    return df

@app.route('/scan', methods=['POST'])
def scan_flat():
    symbols = [s['name'] for s in client.get_symbols()['result'] if 'USDT' in s['name']]
    flat_coins = []
    for symbol in symbols[:50]:
        df = fetch_ohlcv(symbol)
        last_close = df['close'].iloc[-1]
        last_atr = df['ATR'].iloc[-1]
        if last_atr / last_close < 0.005:
            flat_coins.append(symbol)
    if flat_coins:
        msg = "📊 Монети у флеті:\n" + "\n".join(flat_coins)
        send_telegram(msg)
    return "OK", 200

if __name__ == "__main__":
    app.run()
