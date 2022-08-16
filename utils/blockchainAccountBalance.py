from web3 import Web3

class BlockchainBalance:

    def __init__(self, account_handler, base_token, quote_token, endpoint= 'https://api.s0.t.hmny.io'):
        

        self.account_handler = account_handler
        self.endpoint = endpoint

        self.w3 = Web3(Web3.HTTPProvider(self.endpoint))

        self.pointer_to_base_contract = self.w3.eth.contract(
            address= Web3.toChecksumAddress(base_token['address']),
            abi=base_token['abi']
            )

        self.pointer_to_quote_contract = self.w3.eth.contract(
            address= Web3.toChecksumAddress(quote_token['address']),
            abi=quote_token['abi']
            )

    def get_base_token_balance(self):
        
        balance = self.pointer_to_base_contract.functions.balanceOf(self.account_handler.public_key).call() / 10**18
        return balance

    def get_quote_token_balance(self):
        
        balance = self.pointer_to_quote_contract.functions.balanceOf(self.account_handler.public_key).call() / 10**18
        return balance
