import requests
from web3 import Web3

ETHERSCAN_API_KEY = "VJC3HNMXNZJISBZ5V8R11AFT499AB95GX7"

def is_blacklisted(address):
    try:
        address = Web3.to_checksum_address(address)
        url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&apikey={ETHERSCAN_API_KEY}"
        response = requests.get(url).json()

        if "status" in response and response["status"] == "1":
            return "Address has suspicious activity (Reported on Etherscan)"
        return "Address is clean"
    except Exception as e:
        return f"Error checking blacklist: {str(e)}"

def check_chainabuse_blacklist(address):
    url = f"https://api.chainabuse.com/v1/blacklist/{address}"
    headers = {"Authorization": "Bearer YOUR_CHAINABUSE_API_KEY"}
    
    try:
        response = requests.get(url, headers=headers).json()
        if response.get("blacklisted", False):
            return "Address is blacklisted on Chainabuse"
        return "Address is clean"
    except Exception as e:
        return f"Error checking Chainabuse blacklist: {str(e)}"
