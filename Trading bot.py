
import logging
from binance import Client
from binance.exceptions import BinanceAPIException
import time
from datetime import datetime

class SimpleTradingBot:
    
    def __init__(self, api_key, api_secret):
    
        # Set up the connection to binance Testnet (practicemode)
        self.client = Client(api_key, api_secret, testnet=True)
        
        # Set up logging so we see what the bot is doing.
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('trading_bot.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("🤖 Trading Bot initialized on TESTNET (practice mode)")
    
    def get_account_info(self):
        """
        Check how much fake money we have,like checking your piggy bank
        """
        try:
            account = self.client.futures_account()
            balance = float(account['totalWalletBalance'])
            self.logger.info(f"💰 Account Balance: ${balance:.2f} USDT")
            return balance
        except Exception as e:
            self.logger.error(f"❌ Could not get account info: {e}")
            return 0
    def get_current_price(self, symbol):
        """
        Check the current price of a cryptocurrency, like asking "How much does this toy cost?"
        """
        try:
            ticker = self.client.futures_ticker(symbol=symbol)
            price = float(ticker['price'])
            self.logger.info(f"📊 Current price of {symbol}: ${price:.2f}")
            return price
        except Exception as e:
            self.logger.error(f"❌ Could not get price for {symbol}: {e}")
            return None
    
    def place_market_order(self, symbol, side, quantity):
        """
        Place a market order,like saying "I want to buy or sell this right now at current price!"
        
        symbol: What cryptocurrency to trade (like "BTCUSDT" for Bitcoin)
        side: "BUY" or "SELL" , are we buying or selling?
        quantity: How much to buy/sell
        """
        try:
            self.logger.info(f"🚀 Placing MARKET {side} order: {quantity} {symbol}")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantity
            )
            
            self.logger.info(f"✅ Market order placed successfully!")
            self.logger.info(f"Order ID: {order['orderId']}")
            self.logger.info(f"Status: {order['status']}")
            
            return order
            
        except BinanceAPIException as e:
            self.logger.error(f"❌ Binance API Error: {e}")
            return None
        except Exception as e:
            self.logger.error(f"❌ Unexpected error: {e}")
            return None
    
    def place_limit_order(self, symbol, side, quantity, price):
        """
        Place a limit order , like saying "I want to buy/sell, but only at this specific price!"
        
        This is like putting up a sign: "I'll buy this toy, but only if it costs $5 or less"
        """
        try:
            self.logger.info(f"🎯 Placing LIMIT {side} order: {quantity} {symbol} at ${price}")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=Client.ORDER_TYPE_LIMIT,
                timeInForce=Client.TIME_IN_FORCE_GTC,  #Good Till Cancelled
                quantity=quantity,
                price=str(price)
            )
            
            self.logger.info(f"✅ Limit order placed successfully!")
            self.logger.info(f"Order ID: {order['orderId']}")
            self.logger.info(f"Status: {order['status']}")
            
            return order
            
        except BinanceAPIException as e:
            self.logger.error(f"❌ Binance API Error: {e}")
            return None
        except Exception as e:
            self.logger.error(f"❌ Unexpected error: {e}")
            return None
    
    def place_stop_limit_order(self, symbol, side, quantity, stop_price, limit_price):
        """
        BONUS: Stop-Limit Order , like a safety net!
        
        This is like saying: "If the price goes to $100 (stop),  then try to sell at $99 (limit)"
        It helps protect you from losing too much money!
        """
        try:
            self.logger.info(f"🛡️ Placing STOP-LIMIT {side} order: {quantity} {symbol}")
            self.logger.info(f"Stop Price: ${stop_price}, Limit Price: ${limit_price}")
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=Client.ORDER_TYPE_STOP,
                timeInForce=Client.TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=str(limit_price),
                stopPrice=str(stop_price)
            )
            
            self.logger.info(f"✅ Stop-Limit order placed successfully!")
            self.logger.info(f"Order ID: {order['orderId']}")
            
            return order
            
        except BinanceAPIException as e:
            self.logger.error(f"❌ Binance API Error: {e}")
            return None
        except Exception as e:
            self.logger.error(f"❌ Unexpected error: {e}")
            return None

def main():
    """
    Main function ,this is where our program starts!
    """
    print("🤖 Welcome to the Simple Trading Bot!")
    print("📝 This bot uses TESTNET ,no real money involved!")
    print("=" * 50)
    
    API_KEY = "Test.net servers are currently down i couldnt run this"
    API_SECRET = "Test.net servers are currently down i couldnt run this"
    if API_KEY == "":
        print("❌ Please set your API keys first!")
        print("🔗 Get them from: https://testnet.binancefuture.com/")
        return
    
    # Create our trading bot
    bot = SimpleTradingBot(API_KEY, API_SECRET)
    
    # Simple commandline interface
    while True:
        print("\n🎮 What would you like to do?")
        print("1. Check account balance")
        print("2. Check current price")
        print("3. Place market order (buy/sell right now)")
        print("4. Place limit order (buy/sell at specific price)")
        print("5. Place stop-limit order (safety order)")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == "1":
            # Check how much fake money we have
            bot.get_account_info()
            
        elif choice == "2":
            # Check current price of a cryptocurrency
            symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
            bot.get_current_price(symbol)
            
        elif choice == "3":
            #place a market order (buy or sell immediately)
            try:
                symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
                side = input("Enter side (BUY/SELL): ").strip().upper()
                quantity = float(input("Enter quantity: "))
                
                if side in ["BUY", "SELL"]:
                    bot.place_market_order(symbol, side, quantity)
                else:
                    print("❌ Please enter BUY or SELL")
                    
            except ValueError:
                print("❌ Please enter valid numbers")
                
        elif choice == "4":
            # place a limit order (buy/sell at specific price)
            try:
                symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
                side = input("Enter side (BUY/SELL): ").strip().upper()
                quantity = float(input("Enter quantity: "))
                price = float(input("Enter price: "))
                
                if side in ["BUY", "SELL"]:
                    bot.place_limit_order(symbol, side, quantity, price)
                else:
                    print("❌ Please enter BUY or SELL")
                    
            except ValueError:
                print("❌ Please enter valid numbers")
                
        elif choice == "5":
            # Place a stoplimit order (safety order)
            try:
                symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
                side = input("Enter side (BUY/SELL): ").strip().upper()
                quantity = float(input("Enter quantity: "))
                stop_price = float(input("Enter stop price: "))
                limit_price = float(input("Enter limit price: "))
                
                if side in ["BUY", "SELL"]:
                    bot.place_stop_limit_order(symbol, side, quantity, stop_price, limit_price)
                else:
                    print("❌ Please enter BUY or SELL")
                    
            except ValueError:
                print("❌ Please enter valid numbers")
                
        elif choice == "6":
            print("👋 Goodbye! Thanks for using the Simple Trading Bot!")
            break
            
        else:
            print("❌ Please choose a number between 1-6")

if __name__ == "__main__":
    main() 