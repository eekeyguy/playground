import requests
import json
from io import StringIO
import csv
from datetime import datetime

def fetch_coingecko_data():
    url = "https://pro-api.coingecko.com/api/v3/onchain/networks/base/tokens/0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf/pools"
    headers = {
        'accept': 'application/json',
        'x-cg-pro-api-key': 'CG-FNwTw8odvtUP3TViffDhsFfB'
    }
    response = requests.get(url, headers=headers)
    return response.json()

def extract_pool_data(json_data):
    extracted_data = []
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    for pool in json_data['data']:
        attributes = pool['attributes']
        relationships = pool['relationships']
        
        # Extract address from id
        address = pool['id'].split('_')[1] if '_' in pool['id'] else pool['id']
        
        # Extract id from dex
        dex_id = relationships['dex']['data']['id'] if 'dex' in relationships else None

        extracted_data.append({
            'date': current_date,
            'name': attributes['name'],
            'address': address,
            'dex_id': dex_id,
            'token_price_usd': attributes['token_price_usd'],
            'reserve_in_usd': attributes['reserve_in_usd'],
            'h24_buys': attributes['transactions']['h24']['buys'],
            'h24_sells': attributes['transactions']['h24']['sells'],
            'volume_usd_h24': attributes['volume_usd']['h24']
        })
    
    return extracted_data

def convert_to_csv(extracted_data):
    csv_file = StringIO()
    fieldnames = ['date', 'name', 'address', 'dex_id', 'token_price_usd', 'reserve_in_usd', 'h24_buys', 'h24_sells', 'volume_usd_h24']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(extracted_data)
    csv_data = csv_file.getvalue()
    csv_file.close()
    return csv_data

def upload_to_dune(csv_data):
    dune_upload_url = "https://api.dune.com/api/v1/table/upload/csv"
    payload = json.dumps({
        "data": csv_data,
        "description": "Base cbBTC Pool Data",
        "table_name": "Base cbbtc_pool_data",
        "is_private": False
    })
    headers = {
        'Content-Type': 'application/json',
        'X-DUNE-API-KEY': 'p0RZJpTPCUn9Cn7UTXEWDhalc53QzZXV'
    }
    response = requests.post(dune_upload_url, headers=headers, data=payload)
    print(response.text)

def main():
    # Fetch data from CoinGecko API
    json_data = fetch_coingecko_data()
    
    # Extract required pool data
    extracted_data = extract_pool_data(json_data)
    
    # Convert to CSV
    csv_data = convert_to_csv(extracted_data)
    
    # Upload to Dune
    upload_to_dune(csv_data)

if __name__ == "__main__":
    main()
