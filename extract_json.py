"""
Extract and inspect the JSON data from Forbes page
"""
import re
import json

# Read the saved HTML
with open('page_source.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the script containing simple-site data
pattern = r'window\["forbes"\]\["simple-site"\]\s*=\s*({.*?});'
matches = re.findall(pattern, html, re.DOTALL)

if matches:
    print(f"Found {len(matches)} matches")
    json_str = matches[0]
    
    # Save raw JSON string
    with open('raw_json.txt', 'w', encoding='utf-8') as f:
        f.write(json_str)
    
    try:
        data = json.loads(json_str)
        
        # Save pretty JSON
        with open('forbes_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        print("JSON data saved to forbes_data.json")
        
        # Look for company data
        def find_companies(obj, path=""):
            if isinstance(obj, list) and len(obj) > 0:
                if isinstance(obj[0], dict):
                    keys = obj[0].keys()
                    if 'organizationName' in keys or 'company' in str(keys).lower():
                        print(f"\nFound potential companies array at: {path}")
                        print(f"Length: {len(obj)}")
                        print(f"First item keys: {list(obj[0].keys())[:10]}")
                        if len(obj) > 0:
                            print(f"\nFirst company example:")
                            print(json.dumps(obj[0], indent=2)[:500])
            
            if isinstance(obj, dict):
                for key, value in obj.items():
                    find_companies(value, f"{path}.{key}" if path else key)
        
        find_companies(data)
        
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print("First 500 chars of JSON string:")
        print(json_str[:500])
else:
    print("No matches found for simple-site pattern")
    
    # Try alternative patterns
    print("\nTrying to find any JSON-like data with company info...")
    
    # Look for arrays with organization data
    pattern2 = r'\{"organizationName"[^\}]+\}'
    matches2 = re.findall(pattern2, html)
    if matches2:
        print(f"Found {len(matches2)} company-like objects")
        print("First match:")
        print(matches2[0])
