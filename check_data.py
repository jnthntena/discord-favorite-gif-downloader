import json
import base64
import os

def safely_examine_data():
    """Safely examine the data.json file to see what's in the settings"""
    
    if not os.path.exists('data.json'):
        print("No data.json file found")
        return
    
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("=== JSON Structure ===")
        print(f"Top-level keys: {list(data.keys())}")
        
        if 'settings' in data:
            settings = data['settings']
            print(f"\n=== Settings Content ===")
            print(f"Settings type: {type(settings)}")
            print(f"Settings length: {len(str(settings))}")
            
            # Try to decode if it's base64
            try:
                decoded = base64.b64decode(settings).decode('utf-8')
                print(f"\n=== Decoded Settings (first 500 chars) ===")
                print(decoded[:500])
                if len(decoded) > 500:
                    print("... (truncated)")
            except:
                print("Settings is not base64 encoded")
                print(f"Raw settings (first 500 chars): {str(settings)[:500]}")
        
        # Look for URLs in the data
        import re
        all_text = json.dumps(data)
        urls = re.findall(r'https?://[^\s<>"]+', all_text)
        print(f"\n=== URLs Found ({len(urls)}) ===")
        for i, url in enumerate(urls[:10]):  # Show first 10
            print(f"{i+1}. {url}")
        if len(urls) > 10:
            print(f"... and {len(urls) - 10} more URLs")
            
    except Exception as e:
        print(f"Error examining data: {e}")

if __name__ == "__main__":
    safely_examine_data() 