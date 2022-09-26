# Module -1 - Creating the blockchain
# installing flask==0.12.2
# Postman HTTP Client

import hashlib
import datetime
import json
from flask import Flask, request, jsonify

# Building

class Blockchain:
    def __init__(self):
        self.chain = []
        self.data = []
        self.create_block(proof = 1,previous_hash ='0') #Genesis Block
        
    def get_data(self, name, id):
        dataset={
            'customer_id': id, #fetch data from the 
            'name': name
            }
        self.data.append(dataset)
        
        
    def create_block(self, proof, previous_hash): #proof=nonce
        block={ 'index' : len(self.chain)+1,
                'timestamp' : str(datetime.datetime.now()),
                'proof': proof,
                'data': self.data, #list ot tuple of data
                'previous_hash': previous_hash }
        self.chain.append(block)
        return block
        
    def get_previous_block(self):
        return self.chain[-1]
        
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
                # creating a mathematical problem 
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000': #if first four nos are 0s
                    check_proof = True #exits the loop, block successfully mined
            else:
                    new_proof += 1 #trial and error through incrementing
        return new_proof
