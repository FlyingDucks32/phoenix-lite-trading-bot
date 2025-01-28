import schedule  
import time  
from config import SYMBOL, RISK_PER_TRADE  
from utils import get_data, analyze, get_news_sentiment  
from alpaca.trade.client import TradeClient  

def execute_trade():  
    try:  
        df = get_data()  
        df = analyze(df)  
        news_signal = get_news_sentiment()  
        last = df.iloc[-1]  

        # Buy: RSI < 30 + MACD bullish + positive news  
        if last['RSI'] < 30 and last['MACD'] > 0 and news_signal == 'buy':  
            TradeClient().buy(SYMBOL, RISK_PER_TRADE)  

        # Sell: RSI > 70 OR negative news  
        elif last['RSI'] > 70 or news_signal == 'sell':  
            TradeClient().sell_all()  

    except Exception as e:  
        print(f"Error: {e}")  

if __name__ == "__main__":  
    schedule.every(1).hour.do(execute_trade)  
    while True:  
        schedule.run_pending()  
        time.sleep(1)  
