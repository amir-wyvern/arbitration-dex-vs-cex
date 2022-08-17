from web3 import Web3

class BlockchainBalance:

    def __init__(self, account_handler, endpoint= 'https://api.s0.t.hmny.io'):
        

        self.account_handler = account_handler
        self.endpoint = endpoint

        self.w3 = Web3(Web3.HTTPProvider(self.endpoint))

    def fetch_balance(self ,token_contract):
        
        pointer_to_contract = self.w3.eth.contract(
            address= Web3.toChecksumAddress(token_contract['address']),
            abi=token_contract['abi']
            )
        balance = pointer_to_contract.functions.balanceOf(self.account_handler.public_key).call() / 10**18
        return balance

