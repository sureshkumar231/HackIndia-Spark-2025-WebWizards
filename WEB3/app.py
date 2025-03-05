import os
import csv
import hashlib
from flask import Flask, render_template, request, jsonify
from web3 import Web3

app = Flask(__name__, template_folder="templates", static_folder="static")

# Api enga eruku 
ALCHEMY_ETH_URL = "https://eth-mainnet.g.alchemy.com/v2/BypJUUKSl47j4fi1DKjf7tcnkIoy7YYV" # hash requests agum 
web3_eth = Web3(Web3.HTTPProvider(ALCHEMY_ETH_URL))
CONTRACT_ADDRESS = "0x0b86C6155b09a88F3f882ca264B5D585A22452f5"
ABI = [  
    {
        "constant": True,
        "inputs": [{"name": "_hash", "type": "string"}],
        "name": "getCertificateHash",
        "outputs": [{"name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    }
]

try:
    contract = web3_eth.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
except Exception as e:
    print("Error initializing contract:", e)

# File to Store agum genrate panna enga agum
EXCEL_FILE = "generate_details.csv"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate-hash', methods=['POST'])
def generate_hash():
    try:
        data = request.json.get("data")
        if not data:
            return jsonify({"error": "No certificate data provided"}), 400
        
        hash_id = hashlib.sha256(data.encode()).hexdigest()
        save_to_excel(data, hash_id)  # Save to Excel file
        return jsonify({"hash": hash_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/verify-hash/<hash_id>', methods=['GET'])
def verify_hash(hash_id):
    try:
        stored_hash = contract.functions.getCertificateHash(hash_id).call()
        if stored_hash == hash_id:
            return jsonify({"status": "Valid", "hash": hash_id})
        return jsonify({"status": "Invalid", "hash": hash_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def save_to_excel(cert_name, hash_id):
    try:
        file_exists = os.path.isfile(EXCEL_FILE)

        with open(EXCEL_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Certificate Name", "Hash ID"]) 
            writer.writerow([cert_name, hash_id])
    except Exception as e:
        print("Error saving to Excel:", e)

if __name__ == "__main__":
    app.run(debug=True)

#created sureshkumar and webWizards