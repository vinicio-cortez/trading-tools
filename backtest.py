#!/usr/bin/env python3
"""
Simple Backtesting Engine for Trading Strategies
"""

import yfinance as yf
import pandas as pd
import numpy as np
from indicators import calculate_rsi, calculate_macd

def simple_moving_average_strategy(data, short_window=20, long_window=50):
    """
    Simple moving average crossover strategy
    Buy when short MA crosses above long MA
    Sell when short MA crosses below long MA
    """
    data['SMA_Short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_Long'] = data['Close'].rolling(window=long_window).mean()
    
    # Generate signals
    data['Signal'] = 0
    data.loc[data['SMA_Short'] > data['SMA_Long'], 'Signal'] = 1
    data.loc[data['SMA_Short'] < data['SMA_Long'], 'Signal'] = -1
    
    # Position changes
    data['Position'] = data['Signal'].diff()
    
    return data

def rsi_strategy(data, oversold=30, overbought=70):
    """
    RSI mean reversion strategy
    Buy when RSI < oversold
    Sell when RSI > overbought
    """
    data['RSI'] = calculate_rsi(data['Close'])
    
    data['Signal'] = 0
    data.loc[data['RSI'] < oversold, 'Signal'] = 1  # Buy
    data.loc[data['RSI'] > overbought, 'Signal'] = -1  # Sell
    
    data['Position'] = data['Signal'].diff()
    
    return data

def backtest(data, initial_capital=10000, position_size=1.0):
    """
    Run backtest and calculate returns
    """
    if 'Signal' not in data.columns:
        return None
    
    # Calculate daily returns
    data['Returns'] = data['Close'].pct_change()
    
    # Strategy returns
    data['Strategy_Returns'] = data['Signal'].shift(1) * data['Returns']
    
    # Cumulative returns
    data['Cumulative_Returns'] = (1 + data['Returns']).cumprod()
    data['Cumulative_Strategy'] = (1 + data['Strategy_Returns']).cumprod()
    
    # Calculate metrics
    total_return = (data['Cumulative_Strategy'].iloc[-1] - 1) * 100
    buy_and_hold = (data['Cumulative_Returns'].iloc[-1] - 1) * 100
    
    # Number of trades
    trades = data[data['Position'] != 0].shape[0]
    
    # Win rate (simplified)
    winning_trades = data[data['Strategy_Returns'] > 0].shape[0]
    losing_trades = data[data['Strategy_Returns'] < 0].shape[0]
    win_rate = winning_trades / (winning_trades + losing_trades) * 100 if (winning_trades + losing_trades) > 0 else 0
    
    return {
        'total_return': total_return,
        'buy_and_hold_return': buy_and_hold,
        'trades': trades,
        'win_rate': win_rate,
        'winning_trades': winning_trades,
        'losing_trades': losing_trades
    }

def main():
    print("Backtesting Engine")
    print("=" * 50)
    
    # Get user input
    ticker = input("Enter stock ticker (e.g., AAPL): ").strip().upper()
    if not ticker:
        ticker = 'AAPL'
    
    period = input("Period (1y,2y,5y) [default: 1y]: ").strip()
    if not period:
        period = '1y'
    
    print("\nStrategies available:")
    print("1. Moving Average Crossover (20/50)")
    print("2. RSI Mean Reversion (30/70)")
    choice = input("Choose strategy (1 or 2): ").strip()
    
    print(f"\nFetching data for {ticker}...")
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    
    if data.empty:
        print("No data found.")
        return
    
    if choice == '1':
        data = simple_moving_average_strategy(data)
        strategy_name = "Moving Average Crossover"
    else:
        data = rsi_strategy(data)
        strategy_name = "RSI Mean Reversion"
    
    results = backtest(data)
    
    if results:
        print("\n" + "=" * 60)
        print(f"BACKTEST RESULTS: {ticker} - {strategy_name}")
        print("=" * 60)
        print(f"Period: {data.index[0].strftime('%Y-%m-%d')} to {data.index[-1].strftime('%Y-%m-%d')}")
        print(f"Strategy Return: {results['total_return']:.2f}%")
        print(f"Buy & Hold Return: {results['buy_and_hold_return']:.2f}%")
        print(f"Total Trades: {results['trades']}")
        print(f"Win Rate: {results['win_rate']:.1f}%")
        print(f"Winning Trades: {results['winning_trades']}")
        print(f"Losing Trades: {results['losing_trades']}")
        
        if results['total_return'] > results['buy_and_hold_return']:
            print("\n✅ Strategy outperformed buy & hold!")
        else:
            print("\n⚠️ Strategy underperformed buy & hold.")
    
    # Option to save to CSV
    save = input("\nSave results to CSV? (y/n): ").strip().lower()
    if save == 'y':
        filename = f"{ticker}_{strategy_name.replace(' ', '_')}_backtest.csv"
        data.to_csv(filename)
        print(f"Saved to {filename}")

if __name__ == "__main__":
    main()
