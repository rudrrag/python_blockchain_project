# importing libraries
import hashlib
import json
from time import time


class Blockchain(object):
    def __init__(self):
        self.chain = [] # Empty list used to store blockchain
        self.current_transactions = [] # Empty list used to store transactions

    def new_block(self, proof, previous_hash=None):
        # Creates a new Block in the Blockchain
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof, # The proof given by the Proof
            'previous_hash': previous_hash or self.hash(self.chain[-1]) # Hash of the previous hash
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block # Returns a new block

    # Adding a method to add transactions - creates a new transaction to go into the next new mined Block
    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender, # Address of the sender
            'recipient': recipient, # Address of the recipient
            'amount': amount # Amount of the Block that will hold the new transaction
        })
        return self.last_block['index'] + 1 # The index of the Block that will hold the new transactions
    '''
    After new_transaction(), it adds a transaction to the list,
    it returns the index of the block which the transaction will
    be added to-the next one to be mined. This will be useful later on,
    to the user submitting the transaction.
    '''

    '''
    @property lets you call a method like it's a normal attribute
    no brackets needed. Without @property: blockchain.last_block().
    With @property: blockchain.last_block
    '''
    @property
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1]

    '''
    @ - means decorator
    The @staticmethod is used to say that the function doesn't
    need self - the function doesn't care about any particular 
    part of the blockchain, it just does a job with he inputs 
    given. 
    
    Here, hash(block) takes a block and turns it into a hash.
    It doesn't need to know anything about self.chain or
    self.current_transactions - it only needs the block you pase in

    You'd most likely call it like this: Blockchain.hash(some_block)
    No need to create a Blockchain object first.
    '''

    @staticmethod
    def hash(block):
        # Hashes a block
        # We must make sure tht the Dictionary is Ordered,
        # or we'll have inconsisent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


# Understanding Proof of Work
'''
A Proof of Work (PoW) is how new Blocks are created or mined
on the blockchain. The goal of PoW is to discover a numbr which
solves a problem. The numbr must be difficult to find but 
easy to verify - computationally speaking - by anyone on the
network. This is the core idea behind PoW.
'''

# Let's decide the hash of some integer x multiplied by another y
# must end in 0. So hash(x * y_ = ac23d...0
# For this example, let's fix x = 5:
