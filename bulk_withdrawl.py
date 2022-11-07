import pandas as pd
import numpy as np
from eth_account import Account
from web3 import Web3
import csv

# Please input your wallet in test_master.csv
df_master = pd.read_csv('test_master.csv')
MASTER_ADDRESS = df_master['address'][0]
MASTER_PRIVATE_KEY = df_master['Private Key'][0]

GAS_LIMIT = 30000
GAS_PRICE = 25

# Please set it up to your RPC URL
RPC_URL = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# Only withdraw funds from burners which are loaded with gas
file_name = 'loaded_wallets.csv'


def transfer(sender, recipient, value, key):
	nonce = web3.eth.getTransactionCount(sender)
	
	tx = {
		'nonce': nonce,
		'to': recipient,
		'value': web3.toWei(value, 'gwei'),
		'gas': GAS_LIMIT,
		'gasPrice': web3.toWei(GAS_PRICE, 'gwei')
	}
	
	signed_tx = web3.eth.account.sign_transaction(tx, key)
	tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)


def bulk_withdrawl(file_name):
	# Only withdraw funds from burners which are loaded with gas
	df_burners = pd.read_csv(file_name)
	n = df_burners.shape[0]
	
	for i in range(n):
		BURNER_ADDRESS = df_burners['address'][i]
		BURNER_KEY = df_burners['Private Key'][i]
		balance = web3.eth.getBalance(BURNER_ADDRESS) * 10 ** (-9)
		# print(balance)
		value = (balance - GAS_LIMIT * GAS_PRICE)
		# print(BURNER_ADDRESS + ":  "+ str(value) + " Gwei")
		transfer(BURNER_ADDRESS, MASTER_ADDRESS, value, BURNER_KEY)


if __name__ == "__main__":

	bulk_withdrawl(file_name)
	# print(str(web3.eth.getBalance('0x2C3627DC0882b5fe30d5e5C5052Dbca05A2E6976')*10**(-18)))