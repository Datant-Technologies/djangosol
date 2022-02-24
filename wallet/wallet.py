import re
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.transaction import Transaction
from solana.rpc.api import  Client
from solana.system_program import TransferParams, transfer

import json

solana_client = Client('https://api.devnet.solana.com')


def create_wallet(sender_username):
    """
    It creates a new account for the user
    
    :param sender_username: The username of the account that will be sending the payment. By default, this is the email of the user.
    :return: The public key
    """
    try:
        kp = Keypair.generate()
        public_key = str(kp.public_key)
        secret_key = kp.secret_key
        
        data = {
            'public_key': public_key,
            'secret_key': secret_key.decode('latin-1'),
        }
        
        file_name = '{}.txt'.format(sender_username)
        with open(file_name, 'w') as outfile:
            json.dump(data, outfile)
            
        return public_key
    
    except Exception as e:
        print(e)
        return None
    

def load_wallet(sender_username):
    """
    Loads the wallet of the sender from the file
    
    :param sender_username: The username of the sender. By default, this is the email of the user.
    :return: A dictionary with the keys: 'secret_key', 'public_key', 'address', 'balance'
    """
    try:
        file_name = '{}.txt'.format(sender_username)
        with open(file_name) as json_file:
            account = json.loads(json_file)
            account['secret_key'] = account['secret_key'].encode('latin-1')
            return  
        
    except Exception as e:
        print(e)
        return None
    
    
def fund_account(sender_username, amount):
    """
    It funds the account with the amount. 
    :param sender_username: The username of the account that will be sending the tokens. By default, this is the email of the user.
    :param amount: The amount of SOL to airdrop to the specified recipient
    :return: The transaction id of the airdrop.
    """
    try:
        amount = int(1000000000 * amount)
        account = load_wallet(sender_username)
        response = solana_client.request_airdrop(account['public_key'], amount)
        print(response)
        
        transaction_id = response['result']
        if transaction_id != None:
            return transaction_id
        else:
            return None
        
    except Exception as e:
        print('error message:', e)
        return None
    

def get_balance(sender_username):
    """
    Get the balance of a user's wallet
    
    :param sender_username: The username of the account you want to get the balance for. By default, this is the email of the user.
    :return: The balance of the account.
    """
    try:
        account = load_wallet(sender_username)
        response = solana_client.get_balance(account['public_key'])
        print(response)
        
        balance = response['result']['value'] / 1000000000
        
        data = {
            'publicKey': account['public_key'],
            'balance': str(balance),
        }
        
        return data
    
    except  Exception as e:
        print('error: ', e)
        return None
    


def send_sol(sender_username, amount, receiver):
    """
    Send a transaction from a user's wallet to another user
    
    :param sender_username: the username of the person sending the SOL. By default, this is the email of the user initiating the transfer.
    :param amount: The amount of SOL to send
    :param receiver: the public key of the receiver.
    :return: The response from the send_raw_transaction function is a dictionary with a key 'hash'.
    """
    try:
        account = load_wallet(sender_username)
        sender = Keypair.from_secret_key(account['secret_key'])
        amount = int(1000000000 * amount)
        
        txn = Transaction().add(transfer(
                    TransferParams(from_pubkey=sender.public_key, 
                                   to_pubkey=PublicKey(receiver), 
                                   lamports=amount)))
        
        response = solana_client.send_raw_transaction(txn, sender)
        print("Send sol response: {}".format(response))
    
    except Exception as e:
        print('error: ', e)
        return None