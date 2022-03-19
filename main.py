from flask import Flask, render_template
from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet

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

@app.route('/')
def root():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)