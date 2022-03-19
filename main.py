from django.shortcuts import render
from flask import Flask, render_template, request, redirect, url_for, jsonify
from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
import os

# JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
# client = JsonRpcClient(JSON_RPC_URL)



# test_wallet_one = generate_faucet_wallet(client, debug=True)
# test_wallet_two = generate_faucet_wallet(client, debug=True)
# print(test_wallet_one)
# print("=============================================")
# print(test_wallet_two)

# Development Testnet Credentials for xrpl
account_one = {
    "address":"r3ytL5sgRLn7J3qfU3mbztc4eb5hN4ZS3R",
    "secret":"ssuwqQz6pgHyHXf6aY8pYmFapJMqR",
    "sequence_num":26211451
}

account_two = {
    "address":"rBZRJNJ81QLxYrzrgPXiePN25pxTSFEgYQ",
    "secret":"ssvtEeuLTTMAT4iJwJ8qE8oPysLSk",
    "sequence_num":26211506
}


app = Flask(__name__)

def file_encrypt(file_str):
    secret_key = os.environ.get('SECRET_KEY', None)
    if not secret_key:
        return file_str
    else: #@TODO: Encrypt file
        return file_str

def nft_storage_upload(file_str):
    nft_storage_key = os.environ.get('NFT_STORAGE_KEY', None)
    if not nft_storage_key:
        raise Exception("NFT_STORAGE_KEY is not set")
    else: #@TODO: Upload file to NFT Storage
        return "ipfs://hash"

def xcape_encode(ipfs_url):
    return ipfs_url #@TODO: encode ipfs url to xcape url

@app.route('/')
def root():
    return render_template('index.html')
    
@app.route('/mint')
def mint_page():
    return render_template('mint.html')

# Create /encrypt route that receives a file through POST
@app.route('/encrypt', methods=['POST'])
def encrypt_page():
    file = request.files['file']
    filename = file.filename
    file_string = file.read().decode('utf-8')
    encrypted_file_string = file_encrypt(file_string)

    ipfs_link = nft_storage_upload(encrypted_file_string)
    xcape_link = xcape_encode(ipfs_link)

    return render_template('/mint.html', xcape_link=xcape_link)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)