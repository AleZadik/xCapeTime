from cryptography.fernet import Fernet
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS, cross_origin
from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
import requests
import os
from dotenv import load_dotenv
load_dotenv()

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

# Check env mode to build urls correctly
ENV = os.environ.get('ENV', None)
hostname = 'https://xcapetime.herokuapp.com'

if ENV == 'production':
    hostname = os.environ.get('HOSTNAME', None)
else:
    hostname = os.environ.get('LOCALHOST', None)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def file_encrypt(file_str):
    secret_key = os.environ.get('FILE_SECRET_KEY', None)
    if not secret_key:
        return file_str
    else: #@TODO: Encrypt file
        return file_str

def nft_storage_upload(file_from_form):
    nft_storage_key = os.environ.get('NFT_STORAGE_KEY', None)
    if not nft_storage_key:
        raise Exception("NFT_STORAGE_KEY is not set")
    else:
        url = "https://api.nft.storage/upload"
        payload=file_from_form

        headers = {
            'accept': 'application/json',
            'Content-Type': '*/*',
            'Authorization': 'Bearer {}'.format(nft_storage_key)
        }

        response = requests.request("POST", url, headers=headers, data=payload).json()
        cid = response.get('value').get('cid')
        return cid

def xcape_decode(xcape_token):
    xcape_key = os.environ.get('XCAPE_KEY', None)
    if not xcape_key:
        raise Exception("XCAPE_KEY is not set")
    else:
        dec_fun = Fernet(str.encode(xcape_key))
        xcape_cid = dec_fun.decrypt(str.encode(xcape_token))
        return xcape_cid.decode("utf-8")

def xcape_encode(ipfs_url):
    ipfs_cid = ipfs_url.split("/")[-1] # [ipfs:/, /, hash]
    xcape_key = os.environ.get('XCAPE_KEY', None)
    if not xcape_key:
        raise Exception("XCAPE_KEY is not set")
    else:
        enc_fun = Fernet(str.encode(xcape_key))
        xcape_token = enc_fun.encrypt(str.encode(ipfs_cid))
        return xcape_token.decode("utf-8")

# Created route that 'decrypts' the url
@app.route('/unlock/<xcape_link>')
def nft_page(xcape_link):
    xcape_cid = xcape_decode(xcape_link)
    print(xcape_cid)
    # Returns the ipfs link
    return render_template('nft.html', xcape_cid="ipfs://{}".format(xcape_cid))

@app.route('/')
def root():
    return render_template('index.html')

# Create /encrypt route that receives a file through POST
@app.route('/encrypt', methods=['POST'])
def encrypt_page():
    file = request.files['file']
    file_string = file.read()
    encrypted_file_string = file_encrypt(file_string)
    ipfs_link = nft_storage_upload(file_string)
    xcape_link = xcape_encode(ipfs_link)
    
    # Set up the url that will be minted in the XRPL using ipfs & NFT.storage
    nft_mint_url = "{}/unlock/{}".format(hostname, xcape_link)

    return render_template('mint.html', xcape_link=nft_mint_url)

@app.route('/getnfts')
@cross_origin()
def get_nfts():
    return render_template('getnft.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)