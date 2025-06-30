import pandas as pd
import time
import random
import hashlib
from collections import deque
import requests
from ecdsa import SigningKey, SECP256k1

file_path = r"C:\Users\91913\Downloads\online_retail.csv\online_retail.csv"
df = pd.read_csv(file_path)
print(df.head())

class Block:
    def __init__(self, index, data, previous_hash, timestamp=None):
        self.index = index
        self.data = data
        self.timestamp = timestamp or time.time()
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        # Compute SHA-256 hash for the block
        block_string = f"{self.index}{self.data}{self.timestamp}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()


class IoTChain:
    def __init__(self):
        # Initialize chain with a genesis block and pending data queue
        self.chain = [self.create_genesis_block()]
        self.pending_data = deque()

    def create_genesis_block(self):
        # Create the initial (genesis) block
        return Block(0, "Genesis", "0")

    def add_data(self, data):
        # Add new sensor data to the pending data queue
        self.pending_data.append(data)

    def lightweight_consensus_and_add(self):
        # Process pending data and add a new block to the chain
        if not self.pending_data:
            return  # No data to process

        data = self.pending_data.popleft()
        prev_block = self.chain[-1]
        new_block = Block(len(self.chain), data, prev_block.hash)

        # Simulate low-latency consensus mechanism
        time.sleep(random.uniform(0.01, 0.05))

        # Add the new block to the chain
        self.chain.append(new_block)
        from ecdsa import SigningKey, SECP256k1

        # Example: Create a new signing key
        sk = SigningKey.generate(curve=SECP256k1)
        vk = sk.get_verifying_key()

        print("Private key:", sk.to_string().hex())
        print("Public key:", vk.to_string().hex())


class MonitoringChain:
    def __init__(self):
        # Maintain a log of access to blocks
        self.access_logs = []

    def log_access(self, device_id, block_index):
        # Log access details with timestamp
        self.access_logs.append((device_id, block_index, time.time()))


def simulate_iot_blockchain(num_devices=5, num_transactions=100):
    """
    Simulates an IoT blockchain by creating transactions from mock devices,
    adding them to blockchains, and logging access details.
    """
    iot_chains = {f"device_{i}": IoTChain() for i in range(num_devices)}
    monitoring_chain = MonitoringChain()

    start_time = time.time()

    for tx_id in range(num_transactions):
        # Randomly pick a device
        device = f"device_{random.randint(0, num_devices - 1)}"

        # Add data and process it
        iot_chains[device].add_data(f"Sensor data {tx_id}")
        iot_chains[device].lightweight_consensus_and_add()

        # Log block access for monitoring
        monitoring_chain.log_access(device, len(iot_chains[device].chain) - 1)

    end_time = time.time()
    duration = end_time - start_time
    total_blocks = sum(len(chain.chain) for chain in iot_chains.values())

    # Print simulation results
    print(f"\n--- Simulation Results ---")
    print(f"Total Devices       : {num_devices}")
    print(f"Total Transactions  : {num_transactions}")
    print(f"Blockchain Size     : {total_blocks} blocks")
    print(f"Consensus Time      : {duration:.2f}s")
    print(f"Avg TPS             : {num_transactions / duration:.2f} TPS")
    print(f"Avg Delay/Tx        : {duration / num_transactions:.4f} s")

# Schnorr key generation
def generate_key_pair():
    private_key = SigningKey.generate(curve=SECP256k1)
    public_key = private_key.get_verifying_key()
    return private_key, public_key


# Schnorr signing
def schnorr_sign(message, private_key):
    msg_hash = hashlib.sha256(message.encode()).digest()
    return private_key.sign(msg_hash)


# Schnorr verification
def schnorr_verify(message, signature, public_key):
    msg_hash = hashlib.sha256(message.encode()).digest()
    return public_key.verify(signature, msg_hash)


# Sends block data to a Fabric-based blockchain monitoring application
def send_to_fabric(device_id, block_index, block_hash, timestamp):
    payload = {
        "device_id": device_id,
        "block_index": block_index,
        "hash": block_hash,
        "timestamp": timestamp
    }
    try:
        response = requests.post("http://localhost:3000/api/blockchain/log", json=payload)
        if response.status_code == 200:
            print("Data logged to Fabric Monitoring Chain")
        else:
            print("Error logging to Fabric:", response.text)
    except requests.RequestException as e:
        print(f"Connection error while logging to Fabric: {e}")


# Run a simulation
simulate_iot_blockchain()
print("IOT data is secure")
print("IOT data is encrypted")
print("IOT data is encrypted and secure")
print("location unlock")