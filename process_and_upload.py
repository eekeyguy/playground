name: Fetch ETF Data and Upload to Dune

on:
  schedule:
    - cron: '0 0 * * *'  # Runs daily at midnight UTC
  workflow_dispatch:  # Allows manual triggering

jobs:
  fetch-and-upload:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2

    - name: Set up Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '14'

    - name: Install Newman
      run: npm install -g newman

    - name: Run Postman Collection and Save Output
      run: |
        newman run coinmarketcap-api-collection.json --reporter-cli-no-summary --reporter-cli-no-assertions --reporter-cli-no-console > newman_output.txt

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'

    - name: Install Python dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests

    - name: Run Python script
      env:
        DUNE_API_KEY: ${{ secrets.DUNE_API_KEY }}
      run: python process_and_upload.py
