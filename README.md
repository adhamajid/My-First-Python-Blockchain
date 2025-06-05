# My-First-Python-Blockchain
This project is a simple implementation of a blockchain using Python and Flask. The blockchain includes basic features such as proof of work, transactions between users, and a mining system for adding new blocks.

Key Features
Proof of Work: Algorithm for mining new blocks by meeting certain conditions.

Transactions: Users can send transactions to the blockchain.

Block Storage: Each block contains transactions, a hash of the previous block, and a nonce for proof of work.

Mining API: Provides an endpoint for mining new blocks.

Technologies Used
Python

Flask

hashlib

JSON

Running the Application
Prerequisites
Python 3.x

Flask (can be installed via pip install flask)

Installation
Clone this repository to your local machine:

bash
Copy
Edit
git clone https://github.com/username/repository_name.git
Install the required dependencies:

bash
Copy
Edit
pip install flask
Run the application by executing the following Python file:

bash
Copy
Edit
python blockchain.py 5000
You can replace 5000 with your desired port number.

API Endpoints
GET /mine
Mines a new block and adds the existing transactions to it. Returns the latest blockchain status.

Response:

json
Copy
Edit
{
  "message": "Block Successfully Mined",
  "index": 2,
  "hash_of_previous_block": "abcdef123456...",
  "nonce": 345,
  "transactions": [
    {
      "amount": 1,
      "recipient": "node_identifier",
      "sender": "0"
    }
  ]
}
POST /transactions/new
Adds a new transaction to the blockchain. Required data: sender, recipient, and amount.

Request Body:

json
Copy
Edit
{
  "sender": "A",
  "recipient": "B",
  "amount": 10
}
Response:

json
Copy
Edit
{
  "message": "Transaction will be added to block 2"
}
GET /chain
Displays the entire blockchain in JSON format.

Response:

json
Copy
Edit
{
  "chain": [
    {
      "index": 1,
      "timestamp": 1617281329.2724683,
      "transactions": [],
      "hash_of_previous_block": "0",
      "nonce": 0
    },
    {
      "index": 2,
      "timestamp": 1617281362.7372114,
      "transactions": [
        {
          "sender": "A",
          "recipient": "B",
          "amount": 10
        }
      ],
      "hash_of_previous_block": "abcdef123456...",
      "nonce": 345
    }
  ],
  "length": 2
}
Code Explanation
Blockchain Class
hash: Function to generate the hash of a block using SHA-256.

proof_of_work: The algorithm to find a valid nonce that satisfies the "proof of work" condition by brute-forcing until the valid condition is met.

valid_proof: Checks whether the hash of the block and nonce meets the target difficulty.

append_block: Adds a new block to the blockchain and resets the list of transactions.

add_transaction: Adds a new transaction to the blockchain's transaction queue.

API
/mine: Mines a new block and returns the block's details.

/transactions/new: Receives a new transaction and adds it to the blockchain.

/chain: Displays the current state of the blockchain.

Example Usage
Add a new transaction by sending a POST request to /transactions/new:

bash
Copy
Edit
curl -X POST -H "Content-Type: application/json" -d '{"sender": "A", "recipient": "B", "amount": 10}' http://localhost:5000/transactions/new
Mine a new block by sending a GET request to /mine:

bash
Copy
Edit
curl http://localhost:5000/mine
View the current blockchain by sending a GET request to /chain:

bash
Copy
Edit
curl http://localhost:5000/chain
Blockchain Structure Explanation
Genesis Block: The first block created when the blockchain is initialized.

New Blocks: Whenever a new transaction is added, a new block is mined using the proof of work algorithm.

Contribution
If you'd like to contribute, feel free to open an issue or submit a pull request on GitHub.

Suggested Improvements:
In the code self.hash_block(blockchain.last_block), it should be changed to self.hash(self.last_block) to maintain consistency with the hash function name.

In the proof_of_work method, consider adding comments to explain each part of the code for better readability.

Feel free to add further improvements or enhancements based on your future plans for the project.
