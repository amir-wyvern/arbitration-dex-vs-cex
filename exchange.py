import ccxt

class Exchange:

    def __init__(self, account_handler, symbol):
        
        self.mexc = ccxt.mexc({
            'apiKey': account_handler.api_key,
            'secret': account_handler.api_secret
        }) 

        self.symbol = symbol

    def buy_base_token(self):
        pass

    def sell_base_token(self):
        pass

    def get_order_book(self ,limit=3):

        # resp = self.mexc.depth(symbol= self.symbol ,options={ 'limit': limit })
        # return resp
        pass

    def get_current_price(self):
        
        pass
        # resp = client.ticker_price(symbol= self.symbol)
        # return resp


