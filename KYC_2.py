# -*- coding: utf-8 -*-
# Creating the blockchain
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
   
    def hash(self,block):
        #to get the hash of the block
        #converting the block dictionary(array of objects) to a string by using json library
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    
    # ------------------------------------------------------------------------------------------
    
        # Mining, finding the proof of work
        
        # Creating a web app
app = Flask(__name__) # instance of flask class

        
        # Creating a blockchain
blockchain = Blockchain() # making an instance of the class
        
        # Mining the block
@app.route('/mine_block', methods = ['GET','POST'])
def mine_block(): 
        if request.method == 'POST':
            name = request.form.get("name")
            id = request.form.get("id")
            blockchain.get_data(name, id)
            
        previous_block = blockchain.get_previous_block()
        previous_proof = previous_block['proof']
        proof = blockchain.proof_of_work(previous_proof)
        previous_hash = blockchain.hash(previous_block)
        block = blockchain.create_block(proof,previous_hash)
        
        response = {'message': 'Congratulations, you just mined a block',
                        'index': block['index'],
                        'timestamp' : block['timestamp'],
                        'proof': block['proof'],
                        'previous_hash': block['previous_hash']}
        return jsonify(response), 200
        
# getting the full blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)
                }
    return jsonify(response), 200
    

# searching for the customer
@app.route('/search', methods = ['GET'])
def search():
 id = 561
 for i in range(len(blockchain.chain)):
     if blockchain.chain[i].data.customer_id == id:
         response = {
             'name': blockchain.chain[i].data.name
             }
     return jsonify(response), 200

        
        # Running the app
app.run(host = '0.0.0.0', port = 5000)


