

from dex import DexTrade
# from exchange import CexTrade
import logging
from dexUtils.contracts import load_contracs
from dexUtils.account import Account

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


if __name__ == '__main__':

    list_contracts = load_contracs()
    account_handler = Account('defiprivatewyvern@79!'.encode())

    dex = DexTrade(
        public_address=account_handler.getAddress(),
        private_address=account_handler.getPri(),
        base_token_address='0x72cb10c6bfa5624dd07ef608027e366bd690048f',
        quote_token_address='0xe176ebe47d621b984a73036b9da5d834411ef734',
        lp_contract= list_contracts['jewel-busd-lp'],
        router_contract= list_contracts['router'],
        )

    resp = dex.buy_base_token(1*10**18)
    print(resp)
    # exchange = CexTrade()


    #get price of dex
    #get price of exchage

    # if dex / exchage - 1 > 0.06:
    #   buy jewel in exchange 
    #   sell jewel in Dex

    # elif exchage > dex -1 > 0.06 :
    #   sell jewel in exchange:
    #   buy jewel in dex



# 0x38ed17390000000000000000000000000000000000000000000000000de0b6b3a764000000000000000000000000000000000000000000000000000013794c53fe514ac000000000000000000000000000000000000000000000000000000000000000a00000000000000000000000006dc8e55d703c563e4d62cddab12949ec7e4b6e830000000000000000000000000000000000000000000000000000000062fa55eb000000000000000000000000000000000000000000000000000000000000000200000000000000000000000072cb10c6bfa5624dd07ef608027e366bd690048f000000000000000000000000e176ebe47d621b984a73036b9da5d834411ef734

# 1400359904871849472