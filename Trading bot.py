
import logging
from binance import Client
from binance.exceptions import BinanceAPIException
import time
from datetime import datetime

class SimpleTradingBot:
    
    def __init__(self, api_key, api_secret):
    
        # Set up the connection to binance Testnet (practice mode)
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
    