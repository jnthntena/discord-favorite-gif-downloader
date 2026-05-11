import json
import base64
import binascii
import os
import re
from urllib.parse import unquote


def extract_urls(data: bytes) -> list:
    """Mirror of ProtobufParser.extract_urls_simple from main.py"""
    urls = set()

    try:
        text = data.decode('latin-1')
    except Exception:
        text = data.decode('utf-8', errors='ignore')

    url_patterns = [
        r'https?://[^\s"\'\x00-\x1F<>)\]]+',
        r'//[^\s"\'\x00-\x1F<>)\]]+',
    ]

    for pattern in url_patterns:
        for match in re.findall(pattern, text):
            match = match.rstrip('.\'"')
            match = match.split('\\x')[0] if '\\x' in match else match
            match = unquote(match)
            if match.startswith('//'):
                match = 'https:' + match
            if match.startswith(('http://', 'https://')) and len(match) > 10:
                urls.add(match)

    return list(urls)


def safely_examine_data():
    if not os.path.exists('data.json'):
        print("No data.json file found")
        return

    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.loads(f.read())

        print("=== JSON Structure ===")
        print(f"Top-level keys: {list(data.keys())}")

        if 'settings' not in data:
            print("No 'settings' key found in JSON")
            return

        settings = data['settings']
        print(f"\n=== Settings Content ===")
        print(f"Settings type: {type(settings)}")
        print(f"Settings length: {len(str(settings))}")

        # Decode base64 to raw bytes (protobuf binary)
        try:
            protobuf_data = base64.b64decode(settings)
            print(f"Decoded {len(protobuf_data):,} bytes (protobuf binary)")
        except (binascii.Error, ValueError):
            print("Settings is not valid base64, treating as raw text")
            protobuf_data = settings.encode('utf-8')

        # Export raw decoded bytes as latin-1 text so it's inspectable
        with open('decoded_data.txt', 'w', encoding='utf-8', errors='replace') as f:
            f.write("=== DECODED DISCORD DATA ===\n\n")
            f.write(protobuf_data.decode('latin-1'))
        print("\n=== Data exported to 'decoded_data.txt' ===")

        # Extract URLs using the same method as main.py
        urls = extract_urls(protobuf_data)
        print(f"\n=== URLs Found ({len(urls)}) ===")
        for i, url in enumerate(urls[:10], 1):
            print(f"{i}. {url}")
        if len(urls) > 10:
            print(f"... and {len(urls) - 10} more URLs")

        with open('found_urls.txt', 'w', encoding='utf-8') as f:
            f.write("=== FOUND URLs ===\n\n")
            for i, url in enumerate(urls, 1):
                f.write(f"{i}. {url}\n")
        print(f"=== URLs exported to 'found_urls.txt' ===")

    except Exception as e:
        print(f"Error examining data: {e}")


if __name__ == "__main__":
    safely_examine_data()
