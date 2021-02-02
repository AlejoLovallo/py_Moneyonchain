import json
import logging
import logging.config
from web3 import Web3

from moneyonchain.networks import NetworkManager
from moneyonchain.moc import CommissionSplitter

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/31_execute_split.log',
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)


def options_from_settings(filename='settings.json'):
    """ Options from file settings.json """

    with open(filename) as f:
        config_options = json.load(f)

    return config_options


connection_network = 'rskTesnetPublic'
config_network = 'mocTestnetAlpha'

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


# load settings from file
settings = options_from_settings()

contact_address = settings[config_network]['CommissionSplitter']

splitter = CommissionSplitter(network_manager, contract_address=contact_address).from_abi()

info_dict = dict()
info_dict['before'] = dict()
info_dict['after'] = dict()
info_dict['proportion'] = dict()

info_dict['proportion']['moc'] = Web3.fromWei(splitter.moc_proportion(), 'ether')
info_dict['proportion']['multisig'] = 1 - info_dict['proportion']['moc']

print("Splitter address: [{0}]".format(contact_address))
print("Multisig address: [{0}]".format(splitter.commission_address()))
print("MoC address: [{0}]".format(splitter.moc_address()))
print("Proportion MOC: [{0}]".format(info_dict['proportion']['moc']))
print("Proportion Multisig: [{0}]".format(info_dict['proportion']['multisig']))

print("BEFORE SPLIT:")
print("=============")


info_dict['before']['splitter'] = splitter.balance()
print("Splitter balance: [{0}]".format(info_dict['before']['splitter']))

# balances commision
balance = Web3.fromWei(network_manager.network_balance(splitter.commission_address()), 'ether')
info_dict['before']['commission'] = balance
print("Multisig balance (proportion: {0}): [{1}]".format(info_dict['proportion']['multisig'],
                                                         info_dict['before']['commission']))

# balances moc
balance = Web3.fromWei(network_manager.network_balance(splitter.moc_address()), 'ether')
info_dict['before']['moc'] = balance
print("MoC balance (proportion: {0}): [{1}]".format(info_dict['proportion']['moc'],
                                                    info_dict['before']['moc']))


tx_receipt = splitter.split()
if tx_receipt:
    print("Sucessfully splited!")
else:
    print("Error splited!!!")


print("AFTER SPLIT:")
print("=============")

info_dict['after']['splitter'] = splitter.balance()
dif = info_dict['after']['splitter'] - info_dict['before']['splitter']
print("Splitter balance: [{0}] Difference: [{1}]".format(info_dict['after']['splitter'], dif))

# balances commision
balance = Web3.fromWei(network_manager.network_balance(splitter.commission_address()), 'ether')
info_dict['after']['commission'] = balance
dif = info_dict['after']['commission'] - info_dict['before']['commission']
print("Multisig balance (proportion: {0}): [{1}] Difference: [{2}]".format(
    info_dict['proportion']['multisig'],
    info_dict['after']['commission'],
    dif))

# balances moc
balance = Web3.fromWei(network_manager.network_balance(splitter.moc_address()), 'ether')
info_dict['after']['moc'] = balance
dif = info_dict['after']['moc'] - info_dict['before']['moc']
print("MoC balance (proportion: {0}): [{1}] Difference: [{2}]".format(
    info_dict['proportion']['moc'],
    info_dict['after']['moc'],
    dif))


"""

"""