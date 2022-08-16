
from utils.blockchainAccountBalance import BlockchainBalance
from utils.exchangeAccountBalance import ExchanceBalance
from utils.contracts import load_contracs
from utils.account import Account

from dotenv import load_dotenv

from dex import DexTrade
from exchange import Exchange

import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)-24s] [%(levelname)-8s] [%(lineno)-3d -%(name)-7s] | %(message)s',
    handlers=[
    logging.FileHandler("arbit.log"),
    logging.StreamHandler()
    ]
)

class Arbitration:

    def __init__(self):
        pass

    def main(self):
        pass

    
if __name__ == '__main__':

    load_dotenv()
    password = os.getenv('PASSWORD').encode()
    account_keys = Account(password)

    blockchain_balance = BlockchainBalance(account_keys)
    exchange_balance = ExchanceBalance(account_keys)

    list_contracts = load_contracs()
    dex = DexTrade(
        endpoint= 'https://api.s0.t.hmny.io',
        account_keys= account_keys,
        base_token_address= '0x72cb10c6bfa5624dd07ef608027e366bd690048f',
        quote_token_address= '0xe176ebe47d621b984a73036b9da5d834411ef734',
        lp_contract= list_contracts['jewel-busd-lp'],
        router_contract= list_contracts['router']
        )

    exchange = Exchange(account= account_keys)
    
    #get price of dex
    #get price of exchage

    # if dex / exchage - 1 > 0.06:
    #   buy jewel in exchange 
    #   sell jewel in Dex

    # elif exchage > dex -1 > 0.06 :
    #   sell jewel in exchange:
    #   buy jewel in dex
