#!/usr/bin/env python3
"""
Stock Screener - Find stocks with specific technical patterns
"""

import yfinance as yf
import pandas as pd
import sys
from indicators import calculate_all_indicators, get_signals

# List of popular stocks to screen
POPULAR_STOCKS = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA',
    'JPM', 'V', 'WMT', 'JNJ', 'PG', 'UNH', 'HD', 'DIS'
]

def screen_stocks(tickers, period='3mo', interval='1d'):
    """Screen stocks and return those matching criteria"""
    results = []
    
    for ticker in tickers:
        try:
            print(f"Checking {ticker}...")
            stock = yf.Ticker(ticker)
            data = stock.history(period=period, interval=interval)
            
            if len(data) < 50:
                continue
            
            data = calculate_all_indicators(data)
            signals = get_signals(data)
            current_price = data['Close'].iloc[-1]
            
            # Criteria for screening
            is_oversold = signals.get('RSI') == 'OVERSOLD'
            is_bullish_macd = signals.get('MACD') == 'BULLISH_CROSSOVER'
            is_above_sma = signals.get('SMA') == 'ABOVE'
            is_below_lower_bb = signals.get('Bollinger') == 'BELOW_LOWER'
            
            results.append({
                'ticker': ticker,
                'price': current_price,
                'RSI': data['RSI'].iloc[-1],
                'MACD_signal': signals.get('MACD'),
                'RSI_signal': signals.get('RSI'),
                'SMA_signal': signals.get('SMA'),
                'BB_signal': signals.get('Bollinger'),
                'oversold': is_oversold,
                'bullish_macd': is_bullish_macd,
                'above_sma': is_above_sma,
                'below_lower_bb': is_below_lower_bb
            })
        except Exception as e:
            print(f"Error with {ticker}: {e}")
    
    return pd.DataFrame(results)

def main():
    print("Stock Screener")
    print("=" * 50)
    
    # Get user input
    print("\n1. Use default stock list (20 major stocks)")
    print("2. Enter custom tickers (comma-separated)")
    choice = input("Choice (1 or 2): ").strip()
    
    if choice == '2':
        tickers_input = input("Enter tickers (e.g., AAPL,MSFT,TSLA): ").strip().upper()
        tickers = [t.strip() for t in tickers_input.split(',')]
    else:
        tickers = POPULAR_STOCKS
        print(f"Using: {', '.join(tickers)}")
    
    period = input("Period (1mo,3mo,6mo,1y) [default: 3mo]: ").strip()
    if not period:
        period = '3mo'
    
    print(f"\nScreening {len(tickers)} stocks...")
    df = screen_stocks(tickers, period)
    
    if df.empty:
        print("No results found.")
        return
    
    # Display results
    print("\n" + "=" * 80)
    print("SCREENING RESULTS")
    print("=" * 80)
    
    # Show oversold stocks
    oversold = df[df['oversold'] == True]
    if not oversold.empty:
        print("\n📉 OVERSOLD STOCKS (RSI < 30):")
        for _, row in oversold.iterrows():
            print(f"  {row['ticker']}: ${row['price']:.2f} | RSI: {row['RSI']:.1f} | MACD: {row['MACD_signal']}")
    
    # Show bullish MACD crossover
    bullish = df[df['bullish_macd'] == True]
    if not bullish.empty:
        print("\n📈 BULLISH MACD CROSSOVER:")
        for _, row in bullish.iterrows():
            print(f"  {row['ticker']}: ${row['price']:.2f} | MACD: {row['MACD_signal']} | RSI: {row['RSI']:.1f}")
    
    # Show stocks below lower Bollinger Band
    below_bb = df[df['below_lower_bb'] == True]
    if not below_bb.empty:
        print("\n📊 BELOW LOWER BOLLINGER BAND (potential bounce):")
        for _, row in below_bb.iterrows():
            print(f"  {row['ticker']}: ${row['price']:.2f} | BB: {row['BB_signal']}")
    
    # Summary
    print("\n" + "-" * 80)
    print(f"Total stocks screened: {len(df)}")
    print(f"Oversold: {len(oversold)}")
    print(f"Bullish MACD: {len(bullish)}")
    print(f"Below lower BB: {len(below_bb)}")

if __name__ == "__main__":
    main()
