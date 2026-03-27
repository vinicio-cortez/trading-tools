#!/usr/bin/env python3
"""
Discord Chart Bot - Send trading charts to Discord
Requires: pip install discord.py yfinance pandas matplotlib
"""

import discord
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import os
import asyncio
from indicators import calculate_all_indicators, get_signals

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
if not TOKEN:
    print("Error: DISCORD_BOT_TOKEN not set in environment")
    exit(1)
CHANNEL_ID = 1382504908678238245  # Your main channel ID

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def create_chart(ticker, period='3mo'):
    """Create a chart with technical indicators"""
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    
    if data.empty:
        return None
    
    data = calculate_all_indicators(data)
    signals = get_signals(data)
    
    # Create the plot
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    
    # Price with moving averages
    axes[0].plot(data.index, data['Close'], label='Close', color='black', linewidth=1)
    axes[0].plot(data.index, data['SMA'], label='SMA 20', color='blue', linewidth=1)
    axes[0].plot(data.index, data['EMA'], label='EMA 20', color='red', linewidth=1)
    axes[0].fill_between(data.index, data['BB_Lower'], data['BB_Upper'], alpha=0.1, color='gray')
    axes[0].set_title(f'{ticker} - Price with Indicators')
    axes[0].legend(loc='upper left')
    axes[0].grid(True, alpha=0.3)
    
    # RSI
    axes[1].plot(data.index, data['RSI'], color='purple', linewidth=1)
    axes[1].axhline(y=70, color='red', linestyle='--', alpha=0.5)
    axes[1].axhline(y=30, color='green', linestyle='--', alpha=0.5)
    axes[1].fill_between(data.index, 30, 70, alpha=0.1, color='gray')
    axes[1].set_title('RSI (14)')
    axes[1].set_ylim(0, 100)
    axes[1].grid(True, alpha=0.3)
    
    # MACD
    axes[2].plot(data.index, data['MACD'], label='MACD', color='blue', linewidth=1)
    axes[2].plot(data.index, data['MACD_Signal'], label='Signal', color='red', linewidth=1)
    axes[2].bar(data.index, data['MACD_Histogram'], label='Histogram', color='gray', alpha=0.5, width=1)
    axes[2].set_title('MACD')
    axes[2].legend(loc='upper left')
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save to bytes
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    plt.close()
    
    return buf, signals

@client.event
async def on_ready():
    print(f'✅ Discord Chart Bot online as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!chart'):
        parts = message.content.split()
        ticker = parts[1].upper() if len(parts) > 1 else 'AAPL'
        period = parts[2] if len(parts) > 2 else '3mo'
        
        await message.channel.send(f"📊 Generating chart for {ticker}...")
        
        result = create_chart(ticker, period)
        if result:
            buf, signals = result
            await message.channel.send(f"📈 **{ticker}** - {period}\n\n{signals}", file=discord.File(buf, f'{ticker}_chart.png'))
        else:
            await message.channel.send(f"❌ Could not fetch data for {ticker}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!screener'):
        await message.channel.send("🔍 Running stock screener... (This may take a moment)")
        # This would run the screener and send results
        await message.channel.send("Screener coming soon!")

if __name__ == "__main__":
    client.run(TOKEN)
