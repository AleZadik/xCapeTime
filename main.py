from cryptography.fernet import Fernet
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS, cross_origin
from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
import datetime
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
    print(nft_storage_key)
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
        print(response)
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
    # Redirect to /getnfts (User has no actions here.)
    # This can be furthered developed to something more independent
    return redirect(url_for('get_nfts'))

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

@app.route('/nftcheck', methods=['POST'])
@cross_origin()
def nft_check():
    # Get the data from the body
    data = request.get_json()
    memo_data = data.get('MemoData1')
    memo_data_2 = data.get('MemoData2')
    URI = data.get('URI')
    
    if ":" in memo_data: # swap the order if it comes the wrong way
        memo_data, memo_data_2 = memo_data_2, memo_data
    
    # memo_data is formatted as a string "YYYY-MM-DD".
    # memo_data2 is formatted as a string "24:00" representing military time

    # Check if the current date is after the date in the memo_data
    # If it is, then the NFT is valid
    # If it is not, check if the current date is the same as the date in the memo_data
    # If it is, then check if the current time is after the time in the memo_data2 variable
    # If it is, then the NFT is valid
    # If it is not, then the NFT is invalid

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.datetime.now().strftime("%H:%M")

    print("Current Date: {}".format(current_date))
    print("Current Time: {}".format(current_time))

    # Check if the current date is after the date in the memo_data
    if current_date > memo_data:
        encoded_part = URI.split("/")[-1] # Gets the last part of the link
        xcape_cid = xcape_decode(encoded_part)
        ipfs_link = "ipfs://{}".format(xcape_cid)
        return jsonify({"status": "unlocked", "link": ipfs_link})
    elif current_date == memo_data:
        encoded_part = URI.split("/")[-1] # Gets the last part of the link
        xcape_cid = xcape_decode(encoded_part)
        ipfs_link = "ipfs://{}".format(xcape_cid)
        if current_time > memo_data_2:
            return jsonify({"status": "unlocked", "link": ipfs_link})
        else:
            return jsonify({"status": "locked", "link": URI})
    else:
        return jsonify({"status": "locked", "link": URI})



@app.route('/getnfts')
@cross_origin()
def get_nfts():
    return render_template('getnft.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)