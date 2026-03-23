import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import datetime

# পেজ সেটআপ
st.set_page_config(page_title="ETH Pro Signal Bot", layout="wide")

def get_live_data():
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": "ETHUSDT", "interval": "15m", "limit": 100}
    try:
        response = requests.get(url, params=params)
        df = pd.DataFrame(response.json(), columns=['time', 'open', 'high', 'low', 'close', 'vol', 'close_time', 'q_vol', 'trades', 't_base', 't_quote', 'ignore'])
        df['close'] = df['close'].astype(float)
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        return df
    except:
        return None

st.title("🚀 ETH Real-Time Signal Dashboard")

# অটো রিফ্রেশ করার জন্য স্লাইডার বা বাটন
if st.button('Update Data'):
    df = get_live_data()
    if df is not None:
        current_price = df['close'].iloc[-1]
        
        # ক্যালকুলেশন (RSI, EMA, MACD)
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rsi = 100 - (100 / (1 + (gain / loss))).iloc[-1]
        ema_20 = df['close'].ewm(span=20, adjust=False).mean().iloc[-1]
        
        # সিগন্যাল লজিক
        if rsi < 38 and current_price > ema_20:
            signal = "BUY"
            color = "green"
        elif rsi > 62 or current_price < ema_20:
            signal = "SELL"
            color = "red"
        else:
            signal = "WAIT/NEUTRAL"
            color = "gray"

        # ডিসপ্লে সিগন্যাল
        st.markdown(f"<h1 style='text-align: center; color: {color}; font-size: 100px;'>{signal}</h1>", unsafe_allow_html=True)
        
        # প্রাইস এবং ইন্ডিকেটর মেট্রিক্স
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", f"${current_price:.2f}")
        col2.metric("RSI (14)", f"{rsi:.2f}")
        col3.metric("EMA 20", f"${ema_20:.2f}")

        # লাইভ চার্ট
        fig = go.Figure(data=[go.Candlestick(x=df['time'],
                open=df['open'], high=df['high'],
                low=df['low'], close=df['close'])])
        fig.update_layout(title="ETH/USDT 15m Chart", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

st.write("Last updated:", datetime.now().strftime("%H:%M:%S"))
