from eth_account import Account
from web3 import Web3
import csv


def createNewETHWallet(amount):
	"""
	
	:param amount: amount of wallets to create
	:return: list of wallets (json object)
	"""
	
	wallets = []
	
	for id in range(amount):
		account = Account.create('Random  Seed' + str(id))
		privateKey = account._key_obj
		publicKey = privateKey.public_key
		address = publicKey.to_checksum_address()
		
		wallet = {
			"id": id,
			"address": address,
			"privateKey": privateKey,
			"publicKey": publicKey
		}
		wallets.append(wallet.values())
	
	return wallets


def saveETHWallet(jsonData):
	with open('wallets.csv', 'w', newline='') as csv_file:
		csv_writer = csv.writer(csv_file)
		csv_writer.writerow(["id", "address", "Private Key", "Public Key"])
		csv_writer.writerows(jsonData)


if __name__ == "__main__":
	print("---- Start Creating Wallets ----")
	## Please input how many wallets you want to create
	wallets = createNewETHWallet(500)
	saveETHWallet(wallets)
	print("---- Done ----")
