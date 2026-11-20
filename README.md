Blockchain in Python
[insert date] | Rudrra
A beginner-friendly Python project that simulates how a blockchain works - built for portfolio and learning purposes.

About the Project
This project implements a fully working blockchain in Python, exposed over HTTP using Flask.
You can interact with it in real time using a tool like Postman or curl.
What it includes:
 - A Blockchain class that creates blocks, records transactions, and validates the chain.
 - Proof of Work - each new block requires finding a number whose hash starts with four leading zeros
 - Rest API endpoints - mine blocks, post transactions, view the full chain, register nodes, and resolve conflicts
 - Consensus Algorithm - when multiple nodes run the blockchain, the longest valid chain wins
 - Unique node identity using uuid4
 - JSON responses for all API calls
This project builds a simple blockchain from scratch using only Python's standard library - no frameworks,
no third-party packages. It demonstrates the core concepts that make blockchains trustworthy: cryptographic hashing,
block chaining, and tamper detection.

It was built as a portfolio project to explore how decentralised records work under the hood, using Python
as a clear and readable language to show the logic one step at a time.

What it demonstrates:
 - How blocks are created and linked together using SHA-256 hashes
 - How the chain detects if any block's data has been changed
 - How a "genesis block" starts the chain
 - How transaction-like data can be stored in each block

Prerequisites
This project only uses Python's built-in libraries, so there is nothing extra to install.
 - Python 3.7+
 - Git (to clone the repoisitry)
 - pip (comes with python)
 - Flask and Requests (install with: 'pip install flask requests')

Then clone the repositry to get started:
'git clone https://github.com/rudrrag/blockchain-python.git'
'cd blockchain-python'

Running the Project
Run the demo from the project folder:
'python3 main.py'
The API will be available at https://localhost:5000. You can interact with it using Postman or curl.

API Endpoints:
Method| Endpoint | Description |
GET   |     /    | Welcome page |
GET   |   /mine  | Mine a new block |
POST  | /transactions/new | Submit a new transaction |
GET   | /chain            | Return the full blockchain |
POST  | / nodes/register  | Register new peer nodes |
GET   | /nodes/resolve    | Run the consensus algorithm |

Example: Submit a Transaction (Postman)
 1. Set method to POST and URL to http://localhost:5000/transactions/new
 2. Go to the Body tab -> select raw -> set type to JSON
 3. Paste this into the body:
{
    "sender": "john",
    "recipient": "bob",
    "amount": 5
}
 4. Click Send - you should get a 201 response saying which block the transaction will be added to.

Example: Mine a Block (Postman)
 1. Set method to GET and URL to http://localhost:5000/mine
 2. Click Send - you should get a 200 response with the new block's index transactions, proof, and previous hash.
The miner receives 1 coin, sent from address "0" (meaining: newly created coin).
Start the Flask server:
'python3 block_chain.py'
Output:
  * Running on http://0.0.0.0:5000
  * Press CTRL +  C to quit 

Project Structure:
blockchain-python/
└── blockchain.py   # All blockchain logic and Flask API in one file

Code Explanation
Class - Blockchain - Core class: manages the chain, transactions, nodes and consensus
Function - new_block() - Creates and appends a new block to the chain
Function - new_transaction() - Adds a transaction to the pending pool
Function - proof_of_work() - Finds a valid proof by brute force
Function - valid_proof() - Checks if a hash starts with four leading zeros
Function - hash() - SHA-256 hashes a block dictionary
Function - register_nodes() - Adds a peer node URL to the network
Function - valid_chain() - Validates the full chain hash-by-hash
Function - resolve_conflicts() - Fetches peer chains and adopts the longest valid one

Key Concepts
 - Proof of Work: Before a new block can be added, the node must find a number (the "proof") such that when
   it is hashed together with the previous proof, the result starts with four leading zeros (0000...).
   This is computationally hard to find but trivial for anyone else to verify - the same process as Bitcoin.
- Hashing: Each block is hashed using SHA-256. Any changes to a block's data produces a completely different hash,
  making tampering immediately visible. The hash() methods sorts the block's key to ensure consistent output.
- Transactions and Mining: Transactions sit in a pending pool until a block is mined. When /mine is called,
  the pending transactions are bundled into the new block and the miner receives 1 coin.
- Consensus Algorithm: if multiple nodes run this blockchain independently, their chains may diverge.
  When /nodes/resolve is called, the node fetches chains from all registered peers and adopts the longest valid one -
  the rule that keeps the network in agreement.
- Node Identity: Each running instance is assigned a globally unique ID using uuid4, used as the recipient address for mining rewards.

  Author
  Built by Rudrra as a portfolio project.





