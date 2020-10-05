import os
from web3.datastructures import (
    AttributeDict,
)
from hexbytes import HexBytes
from tbtc.constants import contracts
from tbtc.session import setup_logging, init_web3, get_contracts
from tbtc.tbtc_system import TBTC
from tbtc.utils import initialize_contract
from tbtc.bitcoin_helpers import point_to_p2wpkh_address

txhash = "0xb538eabb6cea1fc3af58f1474c2b8f1adbf36a209ec8dc5534618b1f2d860c8e"

node_url = os.getenv("ROPSTEN_URL")
private_key = os.getenv("TBTC_PRIVATE_KEY")
w3 = init_web3(node_url)
version = "1.1.0"
network = "ropsten"
address = 'bc1qzse3hm25w3nx70e8nlss6nlfusj7wd4q3m8gax'

def test_point_to_address():
    receipt = AttributeDict({
        'transactionHash': HexBytes('0xb538eabb6cea1fc3af58f1474c2b8f1adbf36a209ec8dc5534618b1f2d860c8e'), 
        'blockHash': HexBytes('0xefdbdb8a9a2a3cdc9b9dc54979ebbb244d1d2d3c7b74c1c18dbd4882b2af1d29'), 
        'blockNumber': 10920939, 
        'contractAddress': None, 
        'cumulativeGasUsed': 2795145, 
        'from': '0x1bB786eb75DAD46523ea3962E7E3946076f00ff9', 
        'gasUsed': 115281, 
        'logs': [
            AttributeDict({
                'blockHash': HexBytes('0xefdbdb8a9a2a3cdc9b9dc54979ebbb244d1d2d3c7b74c1c18dbd4882b2af1d29'), 
                'address': '0xe20A5C79b39bC8C363f0f49ADcFa82C2a01ab64a', 
                'logIndex': 82, 
                'data': '0x8ecbf801ad1c1e86edf1f274eba7747f86e0aa4b1517d9b65867f9d4bacf15975d9b6e11b9e30776807ce63b8ffd71d44c37411cc9f0c9f0fbadddd7a25c8d85000000000000000000000000000000000000000000000000000000005f6bad46', 
                'removed': False, 
                'topics': [HexBytes('0x8ee737ab16909c4e9d1b750814a4393c9f84ab5d3a29c08c313b783fc846ae33'), HexBytes('0x000000000000000000000000e3584a0872b8d4ba824bb81ed2f108c0d46e1a77')], 
                'blockNumber': 10920939, 
                'transactionIndex': 51, 
                'transactionHash': HexBytes('0xb538eabb6cea1fc3af58f1474c2b8f1adbf36a209ec8dc5534618b1f2d860c8e')})
            ], 
        'logsBloom': HexBytes('0x00000000000000000200008000000004000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000004000'), 
        'status': 1, 
        'to': '0xE3584a0872B8D4Ba824bB81Ed2F108C0d46e1A77', 
        'transactionIndex': 51
        })
    contracts = get_contracts(version, network)
    contract_name = "TBTCSystem"
    tbtcsystem = initialize_contract(w3, contracts[contract_name], contract_name)
    logs = tbtcsystem.events.RegisteredPubkey().processReceipt(receipt)
    assert address == point_to_p2wpkh_address(logs[0]['args']['_signingGroupPubkeyX'], logs[0]['args']['_signingGroupPubkeyY'])


def test_lot_sizes():
    t = TBTC(version, w3, private_key)
    assert len(t.get_available_lot_sizes()) > 0