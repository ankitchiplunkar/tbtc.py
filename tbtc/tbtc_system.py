import logging
from tbtc.session import get_contracts
from tbtc.utils import initialize_contract

logger = logging.getLogger(__name__)

class TBTC():

    def __init__(self, version, web3):
        self.version = version
        self.w3 = web3
        if self.w3.eth.chainId == 1:
            self.network = "mainnet"
        elif self.w3.eth.chainId == 3:
            self.network = "ropsten"
        else:
            raise KeyError(f"Network {self.w3.eth.chainId} not defined")
        self.contracts = get_contracts(self.version, self.network)
        self.tbtc_system = initialize_contract(self.w3, self.contracts["TBTCSystem"], "TBTCSystem")
        logger.info(f"Initialized tBTC with version {self.version}")
    
    def get_available_lot_sizes(self):
        return self.tbtc_system.functions.getAllowedLotSizes().call()
