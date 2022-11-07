import pandas as pd
import numpy as np
from eth_account import Account
from web3 import Web3
import csv

df_master = pd.read_csv('test_master.csv')
MASTER_ADDRESS = df_master['address'][0]
MASTER_PRIVATE_KEY = df_master['Private Key'][0]

# Please set it up to your RPC URL
RPC_URL = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# Gas Set Up
GAS_LIMIT = 30000
GAS_PRICE = 25

file_name = 'loaded_wallets.csv'

def transfer(recipient, value):
	nonce = web3.eth.getTransactionCount(MASTER_ADDRESS)
	
	tx = {
		'nonce': nonce,
		'to': recipient,
		'value': web3.toWei(value, 'ether'),
		'gas': GAS_LIMIT,
		'gasPrice': web3.toWei(GAS_PRICE, 'gwei')
	}
	
	signed_tx = web3.eth.account.sign_transaction(tx, MASTER_PRIVATE_KEY)
	tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
	# print(web3.toHex(tx_hash))

def bulk_transfer(value, n):
	df_burners = pd.read_csv('wallets.csv')
	
	with open('loaded_wallets.csv', 'w', newline='') as csv_file:
		csv_writer = csv.writer(csv_file)
		csv_writer.writerow(["address", "Private Key"])
		
	for i in range(n):
		BURNER_ADDRESS = df_burners['address'][i]
		BURNER_KEY = df_burners['Private Key'][i]
		transfer(BURNER_ADDRESS, value/n)
		
		loaded_wallet = [str(BURNER_ADDRESS), str(BURNER_KEY)]
		with open('loaded_wallets.csv', 'a+', newline='') as csv_file:
			csv_writer = csv.writer(csv_file)
			csv_writer.writerow(loaded_wallet)

if __name__ == "__main__":
	
	bulk_transfer(2,500)