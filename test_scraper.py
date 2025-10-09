"""
Test the Forbes AI 50 scraper with just 2 companies
"""
import sys
sys.path.insert(0, '/workspace')

from forbes_ai50_scraper import scrape_forbes_ai50
import pandas as pd

# Temporarily modify the function to only scrape 2 companies
print("Testing scraper with first 2 companies...")

import requests
from bs4 import BeautifulSoup
import numpy as np
import time
import re
import json
from typing import Dict

from forbes_ai50_scraper import (
    convert_funding_to_number,
    extract_json_from_script,
    scrape_company_detail
)

url = "https://www.forbes.com/lists/ai50/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

print("Fetching Forbes AI 50 main page...")
response = requests.get(url, headers=headers, timeout=30)
response.raise_for_status()

# Extract companies array from the page
companies_json = extract_json_from_script(response.text)

if not companies_json:
    print("Error: Could not extract companies data from page")
    sys.exit(1)

print(f"Found {len(companies_json)} companies in JSON data")

companies_data = []

# Process only first 2 companies for testing
for idx, company in enumerate(companies_json[:2]):
    print(f"\nProcessing {idx + 1}/2: {company.get('organizationName', 'Unknown')}")
    
    company_data = {
        'Name': company.get('organizationName'),
        'What_it_Does': company.get('industry'),
        'Funding': convert_funding_to_number(company.get('funding')),
        'Year_Founded': int(company.get('yearFounded')) if company.get('yearFounded') else np.nan,
        'City': company.get('city'),
        'Country': company.get('country'),
        'Industry': company.get('industry'),
        'CEO': None,
        'Employees': np.nan
    }
    
    # Scrape detailed information from company page
    company_uri = company.get('uri')
    if company_uri:
        details = scrape_company_detail(company_uri, headers)
        company_data['CEO'] = details.get('CEO')
        company_data['Employees'] = details.get('Employees')
    
    # Replace None with np.nan for CEO if still None
    if company_data['CEO'] is None:
        company_data['CEO'] = np.nan
    
    companies_data.append(company_data)

# Create DataFrame
ai_df = pd.DataFrame(companies_data)

# Ensure correct data types
ai_df['Funding'] = ai_df['Funding'].astype('Int64')
ai_df['Year_Founded'] = ai_df['Year_Founded'].astype('Int64')
ai_df['Employees'] = ai_df['Employees'].astype('float')

for col in ['Name', 'What_it_Does', 'City', 'Country', 'Industry', 'CEO']:
    ai_df[col] = ai_df[col].astype('object')

print("\n" + "=" * 80)
print("TEST RESULTS - First 2 companies:")
print("=" * 80)
print(ai_df.to_string())

print("\n" + "=" * 80)
print("Data types:")
print("=" * 80)
print(ai_df.dtypes)

print("\n" + "=" * 80)
print("Expected values (from problem description):")
print("=" * 80)
print("0: Abridge - AI notetaker for doctors - $458000000 - 2018 - San Francisco - United States - Shiv Rao - 301.0")
print("1: Anthropic - AI model developer - $17000000000 - 2020 - San Francisco - United States - Dario Amodei - 1500.0")

print("\n✓ Test complete!")
