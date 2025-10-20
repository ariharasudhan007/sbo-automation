name: SBO Portal Automation

on:
  schedule:
    - cron: '0 */6 * * *'  # Run every 6 hours
  workflow_dispatch:        # Manual trigger

jobs:
  automate-sbo:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y chromium-chromedriver
        python -m pip install --upgrade pip
        pip install selenium pymysql
        
    - name: Run SBO Automation
      run: |
        python main.py
