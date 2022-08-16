from mexc_sdk import Market ,Spot


class Exchange:

    def __init__(self, account_handler, symbol):
        
        self.account_handler = account_handler
        self.symbol = symbol
        self.market = Market(api_key=self.account_handler.api_key, api_secret=self.account_handler.api_secret)

    def buy_base_token(self):
        pass

    def sell_base_token(self):
        pass

    def get_order_book(self ,limit=3):

        resp = client.depth(symbol= self.symbol ,options={ 'limit': limit })
        return resp

    def get_current_price(self):
        
        resp = client.ticker_price(symbol= self.symbol)
        return resp


