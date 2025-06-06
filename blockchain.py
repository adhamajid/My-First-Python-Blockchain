import sys
import hashlib
import json

from time import time
from uuid import uuid4

from flask import Flask, jsonify, request

from urllib.parse import urlparse
import requests

class Blockchain(object):
    difficulty = "0000"  # Difficulty for proof of work

    def hash(self, block):
        block_encoded = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def _init_(self):
        self.chain = []

        self.current_transactions = []

        genesis_hash = self.hash_block("genesis_block")

        self.append_block(
            hash_of_previous_block = genesis_hash,
            nonce = self.proof_of_work(0, genesis_hash, [])
        )

    def proof_of_work(self, index, hash_of_previous_block, transactions) :
        nonce = 0

        while self.valid_proof(index, hash_of_previous_block, transactions, nonce) is False:
            nonce += 1
        return nonce

    def valid_proof(self,index, hash_of_previous_block, transactions, nonce) :
        content = f'{index}{hash_of_previous_block}{transactions}{nonce}'.encode()

        content_hash = hashlib.sha256(content).hexdigest()

        return content_hash[:len(self.difficulty_target)] == self.difficulty_target
    
    def append_block(self, hash_of_previous_block, nonce):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'hash_of_previous_block': hash_of_previous_block,
            'nonce': nonce
        }

        self.current_transactions = []

        self.chain.append(block)

        return block
    
    def add_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'amount': amount,
            'recipient': recipient,
            'sender': sender,
        })

        return self.last_block['index'] + 1
    
    @property
    def last_block(self):
        return self.chain[-1] if self.chain else None
    
app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')
blockchain = Blockchain()
@app.route('/mine', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }

    return jsonify(response), 200

@app.route('/mine', methods=['GET'])
def mine():
    blockchain.add_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    last_block_hash = blockchain.hash_block(blockchain.last_block)
    
    index = len(blockchain.chain)
    nonce = blockchain.proof_of_work(index, last_block_hash, blockchain.current_transactions)

    block = blockchain.append_block(last_block_hash, nonce)

    response = {
        'message': "Block Baru Berhasil Ditambang (mined)",
        'index': block['index'],
        'hash_of_previous_block': block['hash_of_previous_block'],
        'nonce': block['nonce'],
        'transactions': block['transactions'],
    }

    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender', 'recipient', 'amount']

    if not all(k in values for k in required):
        return 'Missing values', 400

    index = blockchain.add_transaction(values['sender'], values['recipient'], values['amount'])

    response = {
        'message': f'Transaksi akan ditambahkan ke blok {index}',
    }
    return jsonify(response), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(sys.argv[1]))