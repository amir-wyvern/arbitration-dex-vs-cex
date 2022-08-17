import ccxt

class ExchanceBalance:
    
    def __init__(self, account_keys, base_token, quote_token):

        self.mexc = ccxt.mexc({
                'apiKey':account_keys.api_key,
                'secret': account_keys.api_secret
            })

    def fetch_balance(self ,symbol):

        resp = self.mexc.fetch_balance()
        if resp['info']['code'] == '200':
            if symbol.upper() not in resp['total']:
                return 0

            return resp['total'][symbol.upper()]

        else:
            raise 'Error response'


