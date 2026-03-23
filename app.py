import pandas as pd
import requests
import time
import os
from datetime import datetime

# --- সেটিংস ---
SYMBOL = "ETHUSDT"
INTERVAL = "15m"  # দ্রুত রেসপন্সের জন্য ১৫ মিনিট সেট করা হয়েছে
TRAILING_PERCENT = 0.01  # ১% দাম বাড়লে স্টপ লস উপরে উঠবে

# পারফরম্যান্স ট্র্যাকিং ফাইল
LOG_FILE = "trade_log.csv"

def get_live_data():
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": SYMBOL, "interval": INTERVAL, "limit": 100}
    try:
        response = requests.get(url, params=params, timeout=10)
        df = pd.DataFrame(response.json(), columns=['time', 'open', 'high', 'low', 'close', 'vol', 'close_time', 'q_vol', 'trades', 't_base', 't_quote', 'ignore'])
        df['close'] = df['close'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None

def log_performance(signal, price):
    # সিগন্যালগুলো একটি ফাইলে সেভ করে রাখবে যাতে পরে চেক করতে পারেন
    if not os.path.isfile(LOG_FILE):
        df = pd.DataFrame(columns=['Time', 'Signal', 'Price'])
        df.to_csv(LOG_FILE, index=False)
    
    new_data = pd.DataFrame([[datetime.now(), signal, price]], columns=['Time', 'Signal', 'Price'])
    new_data.to_csv(LOG_FILE, mode='a', header=False, index=False)

def analyze_advanced(df):
    # RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rsi = 100 - (100 / (1 + (gain / loss))).iloc[-1]
    
    # EMA 20 & 50
    ema_20 = df['close'].ewm(span=20, adjust=False).mean().iloc[-1]
    ema_50 = df['close'].ewm(span=50, adjust=False).mean().iloc[-1]
    
    # MACD
    exp1 = df['close'].ewm(span=12, adjust=False).mean()
    exp2 = df['close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=9, adjust=False).mean()
    
    current_price = df['close'].iloc[-1]
    m_val = macd.iloc[-1]
    s_val = signal_line.iloc[-1]

    print(f"\n--- {SYMBOL} ADVANCED ANALYSIS ---")
    print(f"Price: ${current_price:.2f} | RSI: {rsi:.2f} | MACD: {m_val:.2f}")
    
    # অ্যাডভান্সড সিগন্যাল লজিক
    signal = "🟡 NEUTRAL"
    if rsi < 35 and current_price > ema_20 and m_val > s_val:
        signal = "🚀 STRONG BUY"
    elif rsi > 65 or (current_price < ema_20 and m_val < s_val):
        signal = "⚠️ STRONG SELL"
    
    return signal, current_price

# --- মেইন লুপ ---
print(f"Starting Ultimate Bot for {SYMBOL}...")
last_signal = ""
highest_price = 0

while True:
    df = get_live_data()
    if df is not None:
        signal, price = analyze_advanced(df)
        
        # ট্রেইলিং স্টপ লস কনসেপ্ট (Profit Locking)
        if signal == "🚀 STRONG BUY":
            highest_price = max(highest_price, price)
            trailing_sl = highest_price * (1 - TRAILING_PERCENT)
            print(f"Targeting: {signal} | Trailing SL: ${trailing_sl:.2f}")
        
        # সিগন্যাল চেঞ্জ হলে লগ করা
        if signal != last_signal and signal != "🟡 NEUTRAL":
            print(f"NEW SIGNAL DETECTED: {signal}")
            log_performance(signal, price)
            last_signal = signal

    time.sleep(60) # প্রতি মিনিটে চেক করবে
