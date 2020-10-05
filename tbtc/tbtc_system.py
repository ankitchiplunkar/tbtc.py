import logging
from tbtc.session import (
    init_account,
    get_contracts,
)
from tbtc.utils import initialize_contract

logger = logging.getLogger(__name__)

class TBTC():

    def __init__(self, version, web3, private_key):
        self.version = version
        self.w3 = web3
        if self.w3.eth.chainId == 1:
            self.network = "mainnet"
        elif self.w3.eth.chainId == 3:
            self.network = "ropsten"
        else:
            raise KeyError(f"Network {self.w3.eth.chainId} not defined")
        self.account = init_account(self.w3, private_key)
        self.contracts = get_contracts(self.version, self.network)
        self.system = initialize_contract(self.w3, self.contracts["TBTCSystem"], "TBTCSystem")
        self.deposit_factory = initialize_contract(self.w3, self.contracts["DepositFactory"], "DepositFactory")
        logger.info(f"Initialized tBTC with version {self.version} and network {self.network}")
    

    def get_available_lot_sizes(self):
        return self.system.functions.getAllowedLotSizes().call()

    
    def create_deposit(self, lot_size):
        logger.info("Initiating deposit...")
        value = self.system.functions.getNewDepositFeeEstimate().call()
        create_deposit_call = self.deposit_factory.functions.createDeposit(lot_size)
        receipt = self._manage_transaction(create_deposit_call, gas_limit=1600000, value=value)
        logs = self.system.events.Created().processReceipt(receipt)
        return logs[0]['args']['_depositContractAddress']


    def _manage_transaction(self, function_call, gas_limit, value=0):
        unsigned_txn = function_call.buildTransaction({
            'chainId': self.w3.eth.chainId,
            'nonce': self.w3.eth.getTransactionCount(self.account.address),
            'gas': gas_limit,
            'value': value
        })
        signed_txn = self.w3.eth.account.sign_transaction(
            unsigned_txn, self.account.key)
        tx_hash = self.w3.eth.sendRawTransaction(
            signed_txn.rawTransaction)
        logger.info(f"Sent the transaction {tx_hash.hex()}")
        logger.info("Waiting for transaction to be mined ...")
        return self.w3.eth.waitForTransactionReceipt(tx_hash)

