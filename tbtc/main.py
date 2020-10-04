import os
from tbtc.tbtc_system import TBTC
from tbtc.session import setup_logging, init_web3, get_contracts
from tbtc.utils import initialize_contract

node_url = os.getenv("WEB3_URL")
w3 = init_web3(node_url)
version = "1.1.0"

t = TBTC(version, w3)
t.get_available_lot_sizes()