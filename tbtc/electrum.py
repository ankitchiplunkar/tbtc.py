import socket
import ssl
import json
import time
import errno

class Electrum():
    def __init__(self, host, port, protocol, timeout=5):
        self.host = host
        self.port = port
        self.protocol = protocol
        self.timeout = timeout
        self.connection = None
        self._connect()

    def _connect(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.settimeout(self.timeout)
        if self.protocol=="ssl":
            self.connection = ssl.wrap_socket(self.connection)
        self.connection.connect((self.host, self.port))

    def _receive(self):
        buffer = b""
        is_message_completed = False
        while not is_message_completed:
            buffer += self.connection.recv(1024)
            if buffer.decode("utf-8").endswith("\n"):
                is_message_completed = True
        r = json.loads(buffer)
        return r

    def send(self, method, params):
        payload = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": int(time.time()*1000),
                "method": method,
                "params": params
            }
        ) + '\n'
        payload = payload.encode()
        self.connection.send(payload)
        return self._receive()
    
    def get_latest_block(self):
        method = "blockchain.headers.subscribe"
        params = []
        return self.send(method, params)

    def get_transaction(self, tx_hash, verbose=False):
        method = "blockchain.transaction.get"
        params = [tx_hash]
        if verbose:
            params = params.append(verbose)
        return self.send(method, params)
    
    def get_block_headers(self, block_height, confirmations):
        method = "blockchain.block.headers"
        params = [block_height, confirmations]
        return self.send(method, params)

    def get_transaction_merkle(self, tx_hash, block_height):
        method = "blockchain.transaction.getMerkle"
        params = [tx_hash, block_height]
        return self.send(method, params)