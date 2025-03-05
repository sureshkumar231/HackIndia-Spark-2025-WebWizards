import requests
from web3 import Web3
from etherscan_utils import is_blacklisted

ETHERSCAN_API_KEY = "VJC3HNMXNZJISBZ5V8R11AFT499AB95GX7"

TORNADO_CASH_ADDRESSES = [
    "0x0f8A9b7da05328C5908b6baE9986e7E3fc9Bf47F",
    "0x1F9840a85d5aF5bf1D1762F925BDADdC4201F984"
]

def is_hacked_wallet(address):
    try:
        address = Web3.to_checksum_address(address)
        url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&apikey={ETHERSCAN_API_KEY}"
        response = requests.get(url).json()

        if "result" in response:
            suspicious_senders = []
            for tx in response["result"]:
                sender = tx["from"]
                if is_blacklisted(sender):
                    suspicious_senders.append(sender)

            if suspicious_senders:
                return f"Possible hacked wallet Received funds from blacklisted wallets: {suspicious_senders}"
        return "incoming Transactions ethu inga erukum"
    
    except Exception as e:
        return f"Error checking transactions: {str(e)}"

def check_tornado_cash_usage(address):
    try:
        address = Web3.to_checksum_address(address)
        url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&apikey={ETHERSCAN_API_KEY}"
        response = requests.get(url).json()

        if "result" in response:
            for tx in response["result"]:
                if tx["from"] in TORNADO_CASH_ADDRESSES or tx["to"] in TORNADO_CASH_ADDRESSES:
                    return "Wallet has interacted to Server"
        return "No Tornado Cash interactions"
    
    except Exception as e:
        return f"Error checking Tornado Cash usage: {str(e)}"
