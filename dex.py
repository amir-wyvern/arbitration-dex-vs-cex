from web3._utils.contracts import prepare_transaction ,find_matching_fn_abi
from pyhmy import transaction
from pyhmy import signing 
from pyhmy import account
from time import time 
import logging


"""
btc/usdt

base currency : btc
quote currency : usdt
"""

class DexTrade :

    def __init__(self, endpoint, account_keys,
        base_token_address, quote_token_address, 
        lp_contract, router_contract, slippage= 0.005,
        gas_limit= 10165700, gsa_price= 120*10**9):

        self.base_token_address = base_token_address
        self.quote_token_address = quote_token_address
        self.account_keys = account_keys
        self.slippage = slippage
        self.endpoint = endpoint
        self.gas_limit = gas_limit
        self.gas_price = gsa_price

        self.w3 = Web3(Web3.HTTPProvider(self.endpoint))
        
        self.pointer_to_lp_contract = self.w3.eth.contract(
            address= Web3.toChecksumAddress(lp_contract['address']),
            abi=lp_contract['abi'])

        self.pointer_to_router_contract = self.w3.eth.contract(
            address= Web3.toChecksumAddress( router_contract['address'] ),
            abi=router_contract['abi'])

    def get_base_token_price(self):

        [base_token_amount ,qute_token_amount ,_] = self.pointer_to_lp_contract.functions.getReserves().call()
        base_token_price = qute_token_amount / base_token_amount 

        return base_token_price

    def get_quote_token_price(self):

        [base_token_amount ,qute_token_amount ,_] = self.pointer_to_lp_contract.functions.getReserves().call()
        qute_token_price = base_token_amount / qute_token_amount

        return qute_token_price

    def get_deadLine(self):

        return int(time()) + 10 * 60

    def buy_base_token(self, base_token_amount):

        quote_token_amount = self.get_base_token_price() * base_token_amount
        min_quote_token_amount = int((1 - self.slippage) * quote_token_amount)

        return self._make_trade(
            fn_identifier='swapExactTokensForTokens',
            input_token_amount= base_token_amount,
            output_token_amount= min_quote_token_amount,
            input_token_address= self.base_token_address,
            output_token_addrss= self.quote_token_address
            )

    def sell_base_token(self, base_token_amount):

        quote_token_amount = self.get_base_token_price() * base_token_amount
        max_quote_token_amount = int((1 + self.slippage) * quote_token_amount)

        return self._make_trade(
            fn_identifier='swapTokensForExactTokens',
            input_token_amount= base_token_amount,
            output_token_amount= max_quote_token_amount,
            input_token_address= self.quote_token_address,
            output_token_addrss= self.base_token_address
            )

    def _make_trade(
        self,
        fn_identifier,
        input_token_amount,
        output_token_amount,
        input_token_address,
        output_token_addrss
        ):
            
        deadLine  = self.get_deadLine() 
        
        args = (
            input_token_amount,
            output_token_amount,
            [
                Web3.toChecksumAddress(input_token_address),
                Web3.toChecksumAddress(output_token_addrss)
            ],
            Web3.toChecksumAddress(self.account_keys.public_key),
            deadLine
                )  
        fn_abi = find_matching_fn_abi( self.pointer_to_router_contract.abi ,Web3.codec ,fn_identifier ,args ,())

        rawData = prepare_transaction(
                            self.account_keys.public_key, 
                            Web3,
                            fn_identifier=fn_identifier,
                            contract_abi=self.pointer_to_router_contract.abi,
                            fn_abi=fn_abi,
                            transaction={'to': self.pointer_to_router_contract.address},
                            fn_args=args,
                            fn_kwargs=() 
                            )

        nonce = account.get_account_nonce(self.account_keys.public_key ,block_num='latest' ,endpoint= self.endpoint )
        tx = {  
            'chainId': 1,
            'from': self.account_keys.public_key,
            'gas': self.gas_limit,
            'gasPrice': self.gas_price,
            'data': rawData['data'],
            'nonce': nonce,
            'shardID': 0,
            'to': rawData['to'],
            'toShardID': 0,
            'value': 0
            }

        rawTx = signing.sign_transaction(tx, self.account_keys.private_key).rawTransaction.hex()
        resp_hash = transaction.send_raw_transaction(rawTx, self.endpoint )
        
        logging.info(resp_hash)

        return resp_hash

