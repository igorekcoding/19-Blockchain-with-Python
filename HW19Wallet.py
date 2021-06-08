#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import dependency
import subprocess
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("mnemonic.env")
mnemonic=os.getenv("mnemonic")

# Import constants.py and necessary functions from bit and web3
from constants import *
from web3 import Web3
from web3.middleware import geth_poa_middleware
from decimal import Decimal
from eth_account import Account
from bit import PrivateKeyTestnet
from bit import network

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:3654"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
 
# Create a function called `derive_wallets`
def derive_wallets(coin=BTC, mnemonic=mnemonic, depth=3):
    command = f'php ./derive -g --mnemonic="{mnemonic}" --cols=all --coin={coin} --numderive={depth} --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

# Creates a dictionary object called coins to store the output from `derive_wallets`.
coins = {
    ETH: derive_wallets(coin=ETH),
    BTCTEST: derive_wallets(coin=BTCTEST),
}

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(priv_key, coin):
    if coin == BTCTEST: 
        return PrivateKeyTestnet(str(priv_key))
    elif coin == ETH: 
        return Account.from_key(str(priv_key))

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, to, amount):
    if coin == BTCTEST:
        return account.prepare_transaction(account.address, [(to, amount, BTC)])
    else:
        amount = w3.toWei(Decimal(amount), 'ether')
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": to, "value": amount}
        )
        return {
            "from": account.address,
            "to": to,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
    }

# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, to, amount):
    raw_tx = create_tx(coin, account, to, amount)
    signed_tx = account.sign_transaction(raw_tx)
    if coin == BTCTEST:
        result = network.NetworkAPI.broadcast_tx_testnet(signed_tx)
    else:
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(result.hex())
    return result.hex()

send_tx(BTCTEST, account1, coins[BTCTEST][1]['address'], 0.00003)


account1 = priv_key_to_account(coins[BTCTEST][0]['privkey'], BTCTEST)
account1.address


# In[ ]:




