"""
To run this script need private key, run this scripts with:

user> export ACCOUNT_PK_SECRET=PK
user> python ./reedeem_bpro.py

Where replace with your PK, and also you need to have funds in this account
"""


from decimal import Decimal
from web3 import Web3
from moneyonchain.networks import NetworkManager
from moneyonchain.moc_vendors import VENDORSMoC

connection_network = 'rskTesnetPublic'
config_network = 'mocTestTyD'

# init network manager
# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager = NetworkManager(
    connection_network=connection_network,
    config_network=config_network)

# run install() if is the first time and you want to install
# networks connection from brownie
# network_manager.install()

# Connect to network
network_manager.connect()

moc_main = VENDORSMoC(network_manager).from_abi()

vendor_account = Web3.toChecksumAddress('0x9032f510a5b54a005f04e81b5c98b7f201c4dac1')
amount = Decimal(0.001)

print("Reedem BPro: {0}".format(amount))

# Reedeem BPro
# This transaction is not async, you have to wait to the transaction is mined
print("Please wait to the transaction be mined!...")
tx_receipt = moc_main.reedeem_bpro(amount, vendor_account)

# finally disconnect from network
network_manager.disconnect()