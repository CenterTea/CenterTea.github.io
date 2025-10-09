"""
Quick test to understand the Forbes AI 50 page structure
"""
import requests
from bs4 import BeautifulSoup
import json

url = "https://www.forbes.com/lists/ai50/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

print("Fetching Forbes AI 50 page...")
response = requests.get(url, headers=headers, timeout=30)
print(f"Status code: {response.status_code}")

soup = BeautifulSoup(response.content, 'html.parser')

# Save raw HTML for inspection
with open('page_source.html', 'w', encoding='utf-8') as f:
    f.write(soup.prettify())

print("Page source saved to page_source.html")

# Look for script tags that might contain JSON data
scripts = soup.find_all('script', type='application/ld+json')
print(f"\nFound {len(scripts)} JSON-LD script tags")

# Look for any script tags containing data
all_scripts = soup.find_all('script')
print(f"Found {len(all_scripts)} total script tags")

# Check for common data structures
for script in all_scripts:
    if script.string and ('ai50' in script.string.lower() or 'companies' in script.string.lower()):
        print("\n--- Script with potential data found ---")
        print(script.string[:500])
        break

# Look for tables
tables = soup.find_all('table')
print(f"\nFound {len(tables)} tables")

# Look for list structures
lists = soup.find_all(['ul', 'ol'])
print(f"Found {len(lists)} lists")

# Look for common class patterns
divs_with_company = soup.find_all('div', class_=lambda x: x and ('company' in x.lower() or 'card' in x.lower() or 'item' in x.lower()))
print(f"Found {len(divs_with_company)} divs with company/card/item classes")
