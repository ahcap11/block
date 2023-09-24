import hashlib
import time
import json

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = str(self.index) + self.previous_hash + str(self.timestamp) + json.dumps(self.transactions) + str(self.nonce)
        return hashlib.sha256(data.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", int(time.time()), [])

    def add_block(self, new_block):
        new_block.index = len(self.chain)
        new_block.previous_hash = self.get_last_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def get_last_block(self):
        return self.chain[-1]

    def add_transaction(self, sender, recipient, amount):
        new_transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.get_last_block().transactions.append(new_transaction)

    def build_merkle_tree(self):
        transactions = self.get_last_block().transactions

        if len(transactions) == 0:
            return None

        merkle_tree = transactions.copy()
        while len(merkle_tree) > 1:
            next_level = []
            for i in range(0, len(merkle_tree), 2):
                left = json.dumps(merkle_tree[i])
                right = json.dumps(merkle_tree[i + 1]) if i + 1 < len(merkle_tree) else ''
                combined_hash = hashlib.sha256((left + right).encode()).hexdigest()
                next_level.append(combined_hash)
            merkle_tree = next_level

        return merkle_tree[0]

def is_valid_block(block, previous_block):
    if block.index != previous_block.index + 1:
        return False
    if block.previous_hash != previous_block.hash:
        return False
    if block.calculate_hash() != block.hash:
        return False
    return True
