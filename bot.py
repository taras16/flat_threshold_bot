import ccxt
import pandas as pd
import time, os
from zones import detect_zones
from strategy import breakout_signal

# Завантаження API з оточення
api_key = os.getenv("1gUmXVNesId5CX4H3U")
api_secret = os.getenv("GbRTioFC33wgedomjwWuN1aHDMIP2U3zbHUc ")

exchange = ccxt.bybit({
    "apiKey": api_key,
    "secret": api_secret,
    "enableRateLimit": True
})

symbols = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "XRP/USDT"]  # 🔥 Можна додати більше
timeframe = "15m"

def run_bot():
    while True:
        for symbol in symbols:
            try:
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=200)
                df = pd.DataFrame(ohlcv, columns=["time","open","high","low","close","volume"])

                zones = detect_zones(df)
                last_price = df["close"].iloc[-1]

                breakout = breakout_signal(last_price, zones)
                if breakout:
                    print(f"🚀 Breakout {symbol} near {breakout} at {last_price}")
                    order = exchange.create_market_buy_order(symbol, 0.001)
                    print("✅ Order executed:", order)

            except Exception as e:
                print(f"Error on {symbol}:", e)

        time.sleep(30)  # перевірка раз на 30 секунд

if __name__ == "__main__":
    run_bot()
