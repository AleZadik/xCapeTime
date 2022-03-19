from cryptography.fernet import Fernet
from flask import Flask, render_template, request, redirect, url_for, jsonify
from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
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


app = Flask(__name__)

def file_encrypt(file_str):
    secret_key = os.environ.get('FILE_SECRET_KEY', None)
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

@app.route('/')
def root():
    encoded = xcape_encode("ipfs://bafybeigdyrzt5sfp7udm7hu76uh7y26nf4dfuylqabf3oclgtqy55fbzdi")
    decoded = xcape_decode(encoded)
    print(encoded)
    print("==========================================================")
    print(decoded)
    return render_template('index.html')

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