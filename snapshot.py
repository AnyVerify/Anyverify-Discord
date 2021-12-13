import requests as r

BASE_URL = "https://api.covalenthq.com/v1/250/tokens/"
CONTRACT_ADDRESS = "0xe260bed39020f969bd66b4e2ffcc3c5a34b46a41"
BLOCK_CALL = "/token_holders/?block-height="
PAGE_SIZE = "&page-size=100000&key="
API_KEY = "ADD_COVALENT_API_KEY"
MINIMUM_BALANCE = 1

def get_holders():
    block_endpoint = r.get("https://api.covalenthq.com/v1/250/block_v2/latest/?&key=" + API_KEY)
    block_endpoint = block_endpoint.json()
    block_height = block_endpoint["data"]["items"][0]["height"]
    endpoint = BASE_URL + CONTRACT_ADDRESS + BLOCK_CALL + str(block_height) + PAGE_SIZE + API_KEY
    response = r.get(endpoint)
    token_holders_data = response.json()
    holders = token_holders_data["data"]["items"]
    print(holders)
    holders_address = []

    for holder in holders:
        if(int(holder["balance"])>=MINIMUM_BALANCE):
            holders_address += [holder["address"]]

    return holders_address

get_holders()
