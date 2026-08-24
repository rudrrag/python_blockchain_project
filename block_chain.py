# importing libraries
import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4 # uniquely identifies info/resources
# in computer systems

from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.chain = [] # Empty list used to store blockchain
        self.current_transactions = [] # Empty list used to store transactions

        # Creates the genesis block. Without this, last_block fails
        # because self.chain[-1] has nothing to point to.
        self.new_block(previous_hash='1', proof=100)

    # Understanding Proof of Work
    # Find a number p that when hashes with the previous block's
    # solution a has with 4 leading 0s is produced.

    def proof_of_work(self, last_proof):
        """
        Simple Proof Of Work Algorithm:
        - Find a number p' such that hash (pp') contains 4
        leading zeros, where p is the previous p'
        - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof)
        contain 4 leading zeroes?
        :param last_proof: <int> Previous proof
        :param proof: <int> Current proof
        :return: <bool> True if correct, False if not
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


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

# Flask framework
app = Flask(__name__)
# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/')
def index():
    return '<h1>Welcome to the Blockchain</h1>'

# Creating the mine endpoint which is a GET request
@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work alogorithm to get
    # the next proof
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # We must recieve a reward for finding the proof
    # The sender is "0" to signify that this node has mined
    # a new coin
    blockchain.new_transaction(
        sender='0',
        recipient = node_identifier,
        amount = 1
    )

    # Forge the new block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': f'New Block Forged',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200


# Creating the transaction endpoint which is a POST request,
# since we'll be sending data to it.
@app.route('/transactions/new', methods=['POST'])
def new_transaction():#
    values = request.get_json()

    # Check that the required fields are in the POST data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'],
                                       values['recipient'],
                                       values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

# Creating the chain endpoint,
# which returns the full Blockchain
@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

# Runs the server on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)






