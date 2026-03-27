#!/usr/bin/env python3
"""
Technical Indicators for Trading
Includes RSI, MACD, Bollinger Bands, and Moving Averages
"""

import pandas as pd
import numpy as np

def calculate_sma(prices, window):
    """Simple Moving Average"""
    return prices.rolling(window=window).mean()

def calculate_ema(prices, window):
    """Exponential Moving Average"""
    return prices.ewm(span=window, adjust=False).mean()

def calculate_rsi(prices, window=14):
    """
    Relative Strength Index (RSI)
    Measures the magnitude of recent price changes
    """
    delta = prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=window, min_periods=window).mean()
    avg_loss = loss.rolling(window=window, min_periods=window).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """
    Moving Average Convergence Divergence (MACD)
    Shows relationship between two moving averages
    """
    ema_fast = calculate_ema(prices, fast)
    ema_slow = calculate_ema(prices, slow)
    macd_line = ema_fast - ema_slow
    signal_line = calculate_ema(macd_line, signal)
    histogram = macd_line - signal_line
    
    return {
        'macd': macd_line,
        'signal': signal_line,
        'histogram': histogram
    }

def calculate_bollinger_bands(prices, window=20, num_std=2):
    """
    Bollinger Bands
    Volatility bands placed above and below a moving average
    """
    sma = calculate_sma(prices, window)
    std = prices.rolling(window=window).std()
    upper = sma + (std * num_std)
    lower = sma - (std * num_std)
    
    return {
        'upper': upper,
        'middle': sma,
        'lower': lower
    }

def calculate_all_indicators(data, sma_window=20, ema_window=20, rsi_window=14):
    """
    Calculate all indicators and add to DataFrame
    """
    data['SMA'] = calculate_sma(data['Close'], sma_window)
    data['EMA'] = calculate_ema(data['Close'], ema_window)
    data['RSI'] = calculate_rsi(data['Close'], rsi_window)
    
    macd = calculate_macd(data['Close'])
    data['MACD'] = macd['macd']
    data['MACD_Signal'] = macd['signal']
    data['MACD_Histogram'] = macd['histogram']
    
    bb = calculate_bollinger_bands(data['Close'])
    data['BB_Upper'] = bb['upper']
    data['BB_Middle'] = bb['middle']
    data['BB_Lower'] = bb['lower']
    
    return data

def get_signals(data):
    """Generate trading signals based on indicators"""
    if data is None or data.empty:
        return {}
    
    latest = data.iloc[-1]
    prev = data.iloc[-2] if len(data) > 1 else latest
    
    signals = {}
    
    # RSI signals
    if latest['RSI'] > 70:
        signals['RSI'] = 'OVERBOUGHT'
    elif latest['RSI'] < 30:
        signals['RSI'] = 'OVERSOLD'
    else:
        signals['RSI'] = 'NEUTRAL'
    
    # MACD signals
    if latest['MACD'] > latest['MACD_Signal'] and prev['MACD'] <= prev['MACD_Signal']:
        signals['MACD'] = 'BULLISH_CROSSOVER'
    elif latest['MACD'] < latest['MACD_Signal'] and prev['MACD'] >= prev['MACD_Signal']:
        signals['MACD'] = 'BEARISH_CROSSOVER'
    else:
        signals['MACD'] = 'NO_CROSSOVER'
    
    # Bollinger Bands signals
    if latest['Close'] > latest['BB_Upper']:
        signals['Bollinger'] = 'ABOVE_UPPER'
    elif latest['Close'] < latest['BB_Lower']:
        signals['Bollinger'] = 'BELOW_LOWER'
    else:
        signals['Bollinger'] = 'WITHIN_BANDS'
    
    # Moving Average signals
    if latest['Close'] > latest['SMA']:
        signals['SMA'] = 'ABOVE'
    else:
        signals['SMA'] = 'BELOW'
    
    return signals

if __name__ == "__main__":
    print("Technical Indicators Module")
    print("Available functions:")
    print("  - calculate_sma(prices, window)")
    print("  - calculate_ema(prices, window)")
    print("  - calculate_rsi(prices, window)")
    print("  - calculate_macd(prices, fast, slow, signal)")
    print("  - calculate_bollinger_bands(prices, window, num_std)")
    print("  - calculate_all_indicators(dataframe)")
    print("  - get_signals(dataframe)")
