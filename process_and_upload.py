import json
import requests
import csv
import os
from io import StringIO
from datetime import datetime

def load_newman_output():
    newman_output = os.environ.get('NEWMAN_OUTPUT')
    if not newman_output:
        raise ValueError("Newman output not found in environment variables")
    return json.loads(newman_output)

def extract_etf_data(json_data):
    # Adjust this function based on the actual structure of the API response
    etf_data = json_data.get('data', {}).get('values', [])
    
    extracted_data = []
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    for item in etf_data:
        extracted_data.append({
            'date': current_date,
            'etf_name': item.get('name'),
            'netflow': item.get('netflow')
            # Add more fields as needed
        })
    
    return extracted_data

def convert_to_csv(extracted_data):
    csv_file = StringIO()
    fieldnames = ['date', 'etf_name', 'netflow']  # Modify as needed
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
        "description": "ETF Netflow Data",
        "table_name": "etf_netflow",
        "is_private": False
    })
    headers = {
        'Content-Type': 'application/json',
        'X-DUNE-API-KEY': os.environ['DUNE_API_KEY']
    }
    response = requests.post(dune_upload_url, headers=headers, data=payload)
    print(response.text)

def main():
    try:
        # Load Newman output
        json_data = load_newman_output()
        
        # Extract ETF data
        extracted_data = extract_etf_data(json_data)
        
        # Convert to CSV
        csv_data = convert_to_csv(extracted_data)
        
        # Upload to Dune
        upload_to_dune(csv_data)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()
