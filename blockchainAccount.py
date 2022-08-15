
class Account:

    def __init__(self, public_address, pointer_to_asset_contract, endpoint= 'https://api.s0.t.hmny.io'):
        
        self.public_address = public_address
        self.pointer_to_asset_contract = pointer_to_asset_contract

    def get_balance(self):
        
        balance = self.pointer_to_asset_contract.functions.balanceOf(self.public_address).call() / 10**18
        return balance