import requests
import json

base_url = "http://localhost:3002"

print("Testing MCP Server Endpoints...")
print("=" * 50)

endpoints = [
    "/health",
    "/create_roblox_objects",
    "/get_file_tree",
    "/read_file",
    "/write_file",
    "/create_script"
]

for endpoint in endpoints:
    url = f"{base_url}{endpoint}"
    try:
        if endpoint == "/health":
            response = requests.get(url, timeout=2)
        else:
            response = requests.post(url, json={}, timeout=2)
        
        print(f"✅ {endpoint}: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.text[:100]}")
    except requests.exceptions.RequestException as e:
        print(f"❌ {endpoint}: {str(e)}")

print("\n" + "=" * 50)
print("Test complete!")
