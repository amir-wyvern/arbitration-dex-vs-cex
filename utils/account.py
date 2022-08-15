"""
python version 3.9
"""
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from hashlib import md5
from web3 import Web3
import base64
import redis
import json

import logging
from .utils import Utils


class Account :
    
    __instance = None

    def __init__(self, password):
        
        self.ls_accounts = []
        self.password = password
        self._read_accounts()

    def _read_accounts(self ):

        try :
            with open('./dexUtils/accounts.json' ,'r') as fi:
                ls_account = json.load(fi)    

        except Exception as e:
            logging.error(f'!! error in file accounts.json [{e}]')    
            exit(0)

        if md5(json.dumps(ls_account).encode()).hexdigest() != self.preHash:

            self.ls_accounts = self.decode(ls_account)

            self.preHash = md5(json.dumps(ls_account).encode()).hexdigest()
            logging.info('- accounts updated.')

    def _decode(self ,ls_account):
        
        salt = b'fuckup_' 
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )

        key = base64.urlsafe_b64encode(kdf.derive(self.password) )

        decode_accounts = []
        for index ,acc in enumerate(ls_account) :
            
            if re := {'name', 'pub', 'pri'} - set(acc.keys()) :
                
                logging.error(f"!! can't found keys{re} in index account [{index}]")
                
                continue
                
            name_acc = acc['name']
            pub = ''
            pri = ''
            
            try :
                
                pub = Web3.toChecksumAddress(acc['pub'])

            except Exception as e:
                
                logging.error(f"!! error in public address [{name_acc}] -> [{e}]")
                continue

            try :
                
                pri = Fernet(key).decrypt(acc['pri'].encode()).decode()

                new_acc = {'pub' : pub ,'name':name_acc ,'pri': pri}
                decode_accounts.append(new_acc)
                logging.info(f"- successfully added new account [{name_acc}]")
                
            except Exception as e:
                logging.error(f"!! can't decode private key [{name_acc}] -> [{e}]")
    
        return decode_accounts
    
    @property.getter
    def private_key(self):

        return self.__private_key

    @property.getter
    def public_key(self):

        return self.__public_key
    
    @property.getter
    def api_key(self):

        return self.__api_key

    @property.getter
    def api_secret(self):

        return self.__api_secret

