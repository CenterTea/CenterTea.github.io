"""
Extract company data from Forbes page - improved version
"""
import re
import json

# Read the saved HTML
with open('page_source.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Look for array of companies with organizationName field
# Find the section that contains the company list
pattern = r'\[(\{"naturalId"[^\]]+\})\]'

# Find all scripts
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)

for i, script in enumerate(scripts):
    if 'organizationName' in script and 'yearFounded' in script:
        print(f"Found company data in script {i}")
        
        # Try to find the array of companies
        # Look for pattern like [{"naturalId":...},...]
        matches = re.finditer(r'\[\s*\{\s*"naturalId"[^\]]+\]\s*,', script, re.DOTALL)
        
        for match in matches:
            json_str = match.group(0)[:-1]  # Remove trailing comma
            
            try:
                companies = json.loads(json_str)
                print(f"\nSuccessfully parsed {len(companies)} companies!")
                
                # Save to file
                with open('companies.json', 'w', encoding='utf-8') as f:
                    json.dump(companies, f, indent=2)
                
                print("Companies saved to companies.json")
                
                # Show first company
                if companies:
                    print("\nFirst company:")
                    print(json.dumps(companies[0], indent=2))
                    
                    print("\nSecond company:")
                    print(json.dumps(companies[1], indent=2))
                
                break
                
            except json.JSONDecodeError as e:
                continue
        
        break

# Alternative: just find the array more directly
print("\n\nAlternative extraction method:")
# Find the specific array pattern
match = re.search(r'(\[\{"naturalId":"fred/companies/AI.*?\}\])', html, re.DOTALL)
if match:
    json_str = match.group(1)
    
    # This might be very long, let's try to find just the array boundaries more carefully
    # Look for the pattern that starts with [{"naturalId" and find its closing ]
    
    # Count braces to find matching ]
    start_idx = html.find('[{"naturalId":"fred/companies/AI')
    if start_idx != -1:
        brace_count = 0
        bracket_count = 0
        in_string = False
        escape_next = False
        
        for i in range(start_idx, min(start_idx + 500000, len(html))):
            char = html[i]
            
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
                        json_str = html[start_idx:i+1]
                        print(f"Extracted JSON array of length {len(json_str)} characters")
                        
                        try:
                            companies = json.loads(json_str)
                            print(f"\n✓ Successfully parsed {len(companies)} companies!")
                            
                            with open('companies.json', 'w', encoding='utf-8') as f:
                                json.dump(companies, f, indent=2)
                            
                            print(f"\nFirst company (Abridge):")
                            print(f"  Name: {companies[0].get('organizationName')}")
                            print(f"  Industry: {companies[0].get('industry')}")
                            print(f"  Funding: ${companies[0].get('funding')}M")
                            print(f"  Year Founded: {companies[0].get('yearFounded')}")
                            print(f"  City: {companies[0].get('city')}")
                            print(f"  Country: {companies[0].get('country')}")
                            
                            print(f"\nSecond company (Anthropic):")
                            print(f"  Name: {companies[1].get('organizationName')}")
                            print(f"  Industry: {companies[1].get('industry')}")
                            print(f"  Funding: ${companies[1].get('funding')}M")
                            print(f"  Year Founded: {companies[1].get('yearFounded')}")
                            print(f"  City: {companies[1].get('city')}")
                            print(f"  Country: {companies[1].get('country')}")
                            
                        except json.JSONDecodeError as e:
                            print(f"Error parsing: {e}")
                        
                        break
