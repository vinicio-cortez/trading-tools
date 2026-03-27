#!/usr/bin/env python3
"""
Moving Averages Calculator with Live Stock Data
Fetches real-time stock data from Yahoo Finance
"""

import yfinance as yf
import pandas as pd
import sys

def calculate_sma(prices, window):
    """Calculate Simple Moving Average"""
    return prices.rolling(window=window).mean()

def calculate_ema(prices, window):
    """Calculate Exponential Moving Average"""
    return prices.ewm(span=window, adjust=False).mean()

def get_stock_data(ticker, period='1mo', interval='1d'):
    """
    Fetch stock data from Yahoo Finance
    
    :param ticker: Stock symbol (e.g., 'AAPL', 'SPY')
    :param period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
    :param interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
    :return: DataFrame with stock data
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=period, interval=interval)
        if data.empty:
            print(f"No data found for {ticker}")
            return None
        return data
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return None

def display_moving_averages(data, sma_window=20, ema_window=20):
    """Display moving averages for the last 10 days"""
    if data is None or data.empty:
        return
    
    # Calculate moving averages
    data['SMA'] = calculate_sma(data['Close'], sma_window)
    data['EMA'] = calculate_ema(data['Close'], ema_window)
    
    # Show last 10 days
    recent = data.tail(10)
    
    print("\n" + "="*80)
    print(f"Moving Averages (SMA={sma_window}, EMA={ema_window})")
    print("="*80)
    print(recent[['Close', 'SMA', 'EMA']].round(2).to_string())
    print("="*80)
    
    # Current values
    current_close = data['Close'].iloc[-1]
    current_sma = data['SMA'].iloc[-1]
    current_ema = data['EMA'].iloc[-1]
    
    print(f"\nCurrent Close: ${current_close:.2f}")
    print(f"SMA ({sma_window}): ${current_sma:.2f}")
    print(f"EMA ({ema_window}): ${current_ema:.2f}")
    
    # Trend signals
    if current_close > current_sma:
        print(f"📈 Price is ABOVE SMA — bullish signal")
    else:
        print(f"📉 Price is BELOW SMA — bearish signal")
    
    if current_close > current_ema:
        print(f"📈 Price is ABOVE EMA — bullish signal")
    else:
        print(f"📉 Price is BELOW EMA — bearish signal")

def main():
    print("Stock Moving Averages Calculator")
    print("-" * 40)
    
    # Get user input
    ticker = input("Enter stock ticker (e.g., AAPL, SPY, TSLA): ").strip().upper()
    if not ticker:
        ticker = 'AAPL'
        print(f"Using default: {ticker}")
    
    period = input("Period (1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,max) [default: 3mo]: ").strip()
    if not period:
        period = '3mo'
    
    sma_window = input("SMA window (days) [default: 20]: ").strip()
    sma_window = int(sma_window) if sma_window else 20
    
    ema_window = input("EMA window (days) [default: 20]: ").strip()
    ema_window = int(ema_window) if ema_window else 20
    
    print(f"\nFetching data for {ticker}...")
    data = get_stock_data(ticker, period=period)
    
    if data is not None:
        display_moving_averages(data, sma_window, ema_window)

if __name__ == "__main__":
    main()
