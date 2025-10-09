"""
Inspect a company detail page to understand structure
"""
import requests
from bs4 import BeautifulSoup
import re
import json

url = "https://www.forbes.com/companies/abridge/?list=ai50"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

print(f"Fetching {url}...")
response = requests.get(url, headers=headers, timeout=30)
soup = BeautifulSoup(response.content, 'html.parser')

# Save the page
with open('abridge_page.html', 'w', encoding='utf-8') as f:
    f.write(soup.prettify())

print("Page saved to abridge_page.html")

# Look for JSON data
scripts = soup.find_all('script')
for i, script in enumerate(scripts):
    if script.string and ('ceo' in script.string.lower() or 'employee' in script.string.lower()):
        print(f"\n--- Script {i} with CEO/Employee data ---")
        print(script.string[:1000])
        
        # Try to find JSON
        if '{' in script.string:
            # Look for CEO field
            ceo_match = re.search(r'"ceo":\s*"([^"]+)"', script.string, re.I)
            if ceo_match:
                print(f"\nFound CEO in JSON: {ceo_match.group(1)}")
            
            # Look for employees field
            emp_match = re.search(r'"employees?":\s*(\d+(?:\.\d+)?)', script.string, re.I)
            if emp_match:
                print(f"Found Employees in JSON: {emp_match.group(1)}")

# Look for text containing CEO name
page_text = soup.get_text()
shiv_match = re.search(r'(Shiv\s+Rao)', page_text)
if shiv_match:
    print(f"\n✓ Found 'Shiv Rao' in page text")
    # Get context
    start = max(0, shiv_match.start() - 100)
    end = min(len(page_text), shiv_match.end() + 100)
    print(f"Context: ...{page_text[start:end]}...")

# Look for employee count
emp_match = re.search(r'301', page_text)
if emp_match:
    print(f"\n✓ Found '301' in page text")
    start = max(0, emp_match.start() - 100)
    end = min(len(page_text), emp_match.end() + 100)
    print(f"Context: ...{page_text[start:end]}...")

# Try to find structured data
print("\n\nLooking for structured data (dl, table, etc.)...")
for dl in soup.find_all('dl')[:5]:
    print(f"\nDefinition list found:")
    print(dl.get_text()[:200])

for table in soup.find_all('table')[:5]:
    print(f"\nTable found:")
    print(table.get_text()[:200])
