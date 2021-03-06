from moneyonchain.manager import ConnectionManager
from moneyonchain.changers import MocInrateBitProInterestChanger

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger('default')


network = 'mocTestnetAlpha'
connection_manager = ConnectionManager(network=network)
print("Connecting to %s..." % network)
print("Connected: {conectado}".format(conectado=connection_manager.is_connected))

contract = MocInrateBitProInterestChanger(connection_manager)
block_span = 3000

if network in ['mocTestnetAlpha']:
    execute_change = True
else:
    execute_change = False

tx_hash, tx_receipt = contract.constructor(block_span, execute_change=execute_change)
if tx_receipt:
    print("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))
else:
    print("Error deploying changer")


"""

"""