import os
from tbtc.tbtc_system import TBTC
from tbtc.session import setup_logging, init_web3, get_contracts
from tbtc.utils import initialize_contract

setup_logging()
node_url = os.getenv("ROPSTEN_URL")
private_key = os.getenv("TBTC_PRIVATE_KEY")
w3 = init_web3(node_url)
version = "1.1.0"

t = TBTC(version, w3, private_key)
lot_sizes = t.get_available_lot_sizes()
logs = t.create_deposit(lot_sizes[0])