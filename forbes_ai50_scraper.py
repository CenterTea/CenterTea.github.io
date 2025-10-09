"""
Forbes AI 50 Companies Web Scraper
This script scrapes company information from Forbes AI 50 list
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import re
import json
from typing import Dict, List, Optional

def convert_funding_to_number(funding: Optional[float]) -> Optional[int]:
    """
    Convert funding to actual number in dollars
    The JSON provides funding in millions
    """
    if funding is None or pd.isna(funding):
        return np.nan
    
    # Funding in JSON is already in millions, convert to dollars
    return int(funding * 1000000)

def extract_json_from_script(html_content: str) -> Optional[List[Dict]]:
    """
    Extract the companies array from the Forbes page JavaScript
    """
    # Find the array of companies with organizationName field
    start_idx = html_content.find('[{"naturalId":"fred/companies/AI')
    
    if start_idx == -1:
        return None
    
    # Count brackets to find matching ]
    bracket_count = 0
    in_string = False
    escape_next = False
    
    for i in range(start_idx, min(start_idx + 500000, len(html_content))):
        char = html_content[i]
        
        if escape_next:
            escape_next = False
            continue
            
        if char == '\\':
            escape_next = True
            continue
        
        if char == '"' and not escape_next:
            in_string = not in_string
            continue
        
        if not in_string:
            if char == '[':
                bracket_count += 1
            elif char == ']':
                bracket_count -= 1
                if bracket_count == 0:
                    # Found the end
                    json_str = html_content[start_idx:i+1]
                    try:
                        companies = json.loads(json_str)
                        return companies
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON: {e}")
                        return None
    
    return None

def scrape_company_detail(company_uri: str, headers: Dict) -> Dict:
    """
    Scrape detailed information from individual company page
    Returns: dict with CEO and Employees
    """
    try:
        company_url = f"https://www.forbes.com/companies/{company_uri}/?list=ai50"
        print(f"  Fetching detail page: {company_uri}")
        time.sleep(1.5)  # Pause 1-2 seconds
        
        response = requests.get(company_url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        details = {
            'CEO': None,
            'Employees': np.nan
        }
        
        # Look for JSON-LD structured data (most reliable)
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        for script in json_ld_scripts:
            if script.string:
                try:
                    data = json.loads(script.string)
                    if isinstance(data, dict) and data.get('@type') == 'Organization':
                        # Extract CEO
                        if 'employee' in data and isinstance(data['employee'], dict):
                            if data['employee'].get('jobTitle', '').lower() == 'ceo':
                                details['CEO'] = data['employee'].get('name')
                        
                        # Extract Employees
                        if 'numberOfEmployees' in data:
                            emp_value = data['numberOfEmployees']
                            if emp_value:
                                try:
                                    details['Employees'] = float(str(emp_value).replace(',', ''))
                                except:
                                    pass
                        
                        # If we found the data, we're done
                        if details['CEO'] or not pd.isna(details['Employees']):
                            return details
                except (json.JSONDecodeError, ValueError):
                    continue
        
        # Fallback: Try to parse from page text if JSON-LD didn't work
        page_text = soup.get_text()
        
        if not details['CEO']:
            # Try to find CEO in text
            ceo_patterns = [
                r'CEO\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            ]
            for pattern in ceo_patterns:
                match = re.search(pattern, page_text)
                if match:
                    details['CEO'] = match.group(1).strip()
                    break
        
        if pd.isna(details['Employees']):
            # Try to find Employees in text
            emp_match = re.search(r'Employees\s*(\d+(?:,\d{3})*)', page_text)
            if emp_match:
                try:
                    details['Employees'] = float(emp_match.group(1).replace(',', ''))
                except:
                    pass
        
        return details
        
    except Exception as e:
        print(f"  Error scraping company detail {company_uri}: {str(e)}")
        return {
            'CEO': None,
            'Employees': np.nan
        }

def scrape_forbes_ai50() -> pd.DataFrame:
    """
    Main function to scrape Forbes AI 50 list
    Returns: DataFrame with all companies' information
    """
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
        return pd.DataFrame()
    
    print(f"Found {len(companies_json)} companies in JSON data")
    
    companies_data = []
    
    # Process each company
    for idx, company in enumerate(companies_json[:50]):  # Limit to 50
        print(f"\nProcessing {idx + 1}/50: {company.get('organizationName', 'Unknown')}")
        
        company_data = {
            'Name': company.get('organizationName'),
            'What_it_Does': company.get('industry') or company.get('description', '').split('.')[0] if company.get('description') else None,
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
        
        # Replace None with np.nan for CEO and Employees if still None
        if company_data['CEO'] is None:
            company_data['CEO'] = np.nan
        
        companies_data.append(company_data)
    
    # Create DataFrame
    ai_df = pd.DataFrame(companies_data)
    
    # Ensure correct data types according to specifications
    # Funding: int
    ai_df['Funding'] = ai_df['Funding'].astype('Int64')  # Nullable integer
    
    # Year_Founded: int
    ai_df['Year_Founded'] = ai_df['Year_Founded'].astype('Int64')  # Nullable integer
    
    # Employees: float
    ai_df['Employees'] = ai_df['Employees'].astype('float')
    
    # All other columns: object
    for col in ['Name', 'What_it_Does', 'City', 'Country', 'Industry', 'CEO']:
        ai_df[col] = ai_df[col].astype('object')
    
    return ai_df

if __name__ == "__main__":
    print("=" * 60)
    print("Forbes AI 50 Scraper")
    print("=" * 60)
    
    ai_df = scrape_forbes_ai50()
    
    print("\n" + "=" * 60)
    print(f"Successfully scraped {len(ai_df)} companies")
    print("=" * 60)
    
    print("\nFirst 2 companies:")
    print(ai_df.head(2).to_string())
    
    print("\nData types:")
    print(ai_df.dtypes)
    
    # Save to CSV
    ai_df.to_csv('ai50_companies.csv', index=False)
    print(f"\nData saved to ai50_companies.csv")
