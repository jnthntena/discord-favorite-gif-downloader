import json
import base64
import binascii
import os

def safely_examine_data():
    """Safely examine the data.json file to see what's in the settings"""
    
    if not os.path.exists('data.json'):
        print("No data.json file found")
        return
    
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            content = f.read()
            data = json.loads(content)
        
        print("=== JSON Structure ===")
        print(f"Top-level keys: {list(data.keys())}")
        
        if 'settings' in data:
            content = data['settings']
            print(f"\n=== Settings Content ===")
            print(f"Settings type: {type(content)}")
            print(f"Settings length: {len(str(content))}")
            
            # Try to decode if it's base64
            try:
                decoded_content = base64.b64decode(content).decode('utf-8', errors='ignore')
                # Check if the decoded content is actually meaningful (contains readable text)
                if len(decoded_content.strip()) < 10 or not any(c.isalpha() for c in decoded_content):
                    # Decode succeeded but result is not meaningful, treat as not base64
                    print("Settings is not base64 encoded (decoded but not meaningful)")
                    print(f"Raw settings (first 500 chars): {str(content)[:500]}")
                    decoded_content = content
                else:
                    print("Settings appears to be base64 encoded")
                    # print(f"\n=== Decoded Settings (first 500 chars) ===")
                    # print(decoded_content[:500])
                    # if len(decoded_content) > 500:
                    #     print("... (truncated)")
            except (binascii.Error, UnicodeDecodeError):
                print("Settings is not base64 encoded")
                print(f"Raw settings (first 500 chars): {str(content)[:500]}")
                decoded_content = content

        # Export the decoded content to a file
        export_filename = "decoded_data.txt"
        with open(export_filename, 'w', encoding='utf-8') as f:
            f.write("=== DECODED DISCORD DATA ===\n\n")
            f.write(decoded_content)
        print(f"\n=== Data exported to '{export_filename}' ===")
        
        # Look for URLs in the data using the same pattern as main.py
        import re
        pattern = r'https?:?/+[a-zA-Z0-9\-._~:/?#[\]@!$&\'()*+,;=%]+'
        urls = re.findall(pattern, decoded_content)
        print(f"\n=== URLs Found ({len(urls)}) ===")
        for i, url in enumerate(urls[:10]):  # Show first 10
            print(f"{i+1}. {url}")
        if len(urls) > 10:
            print(f"... and {len(urls) - 10} more URLs")
            
        # Also export URLs to a separate file
        urls_filename = "found_urls.txt"
        with open(urls_filename, 'w', encoding='utf-8') as f:
            f.write("=== FOUND URLs ===\n\n")
            for i, url in enumerate(urls, 1):
                f.write(f"{i}. {url}\n")
        print(f"=== URLs exported to '{urls_filename}' ===")
            
    except Exception as e:
        print(f"Error examining data: {e}")

if __name__ == "__main__":
    safely_examine_data() 