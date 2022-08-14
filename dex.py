from time import sleep ,time ,mktime
import requests
from contracts import load_contracs
from web3 import Web3
import logging
from datetime import datetime
from web3._utils.contracts import prepare_transaction ,find_matching_fn_abi
from time import time
from account import Account
from utils import Utils
from pyhmy import signing 
from pyhmy import account
from pyhmy import transaction

class DexTrade :

    def __init__(self):

        self.list_contracts = loadContracs()
        self.w3 = Web3(Web3.HTTPProvider('https://api.s0.t.hmny.io'))
        self.slippage = 0.01
        self.initial_contracts()

    def initial_contracts(self):

        self.pointer_to_jewelBusd_contract = w3.eth.contract(
            address= Web3.toChecksumAddress(self.list_contracts['jewel-busd-lp']['address']),
            abi=self.list_contracts['jewel-busd-lp']['abi'])

        self.pointer_to_router_contract = w3.eth.contract(
            address= Web3.toChecksumAddress( self.list_contracts['router']['address'] ),
            abi=self.list_contracts['router']['abi'])

    def get_base_token_price(self):

        [jewel_amount ,busd_amount ,_] = self.pointer_to_jewelBusd_contract.getReserves().call()
        jewel_busd_price = busd_amount / jewel_amount 

        return jewel_busd_price

    def get_quote_token_price(self):

        [jewel_amount ,busd_amount ,_] = self.pointer_to_jewelBusd_contract.getReserves().call()
        busd_jewel_price = jewel_amount / busd_amount

        return busd_jewel_price

    def get_deadLine(self):

        return int(time()) + 10 * 60

    def buy_base_token(self, base_token_amount):

        deadLine  = self.get_deadLine()
        quote_token_amount = int(base_token_amount * self.get_base_token_price())
        min_quote_token_amount = (1 - self.slippage) * quote_token_amount

    def sell_base_token(self, base_token_amount):

        deadLine  = self.get_deadLine() 
        quote_token_amount = int(base_token_amount * self.get_base_token_price()) 
        min_quote_token_amount = (1 - self.slippage) * quote_token_amount

