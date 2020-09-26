import os
from tbtc.contracts import contracts
from tbtc.session import setup_logging, init_web3
from tbtc.utils import initialize_contract

node_url = os.getenv("WEB3_URL")
w3 = init_web3(node_url)
version = "1.1.0"

contract_name = "TBTCSystem"
tbtcsystem = initialize_contract(w3, contracts[version]["mainnet"][contract_name], contract_name)