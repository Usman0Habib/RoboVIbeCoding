import requests
import json

class MCPClient:
    def __init__(self, base_url='http://localhost:3002'):
        self.base_url = base_url
        self.connected = False
    
    def check_connection(self):
        try:
            response = requests.get(f"{self.base_url}/health", timeout=2)
            self.connected = response.status_code == 200
            return self.connected
        except:
            self.connected = False
            return False
    
    def get_file_tree(self):
        try:
            response = requests.post(
                f"{self.base_url}/get_file_tree",
                json={},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'Failed to get file tree: {str(e)}', 'tree': []}
    
    def read_file(self, path):
        try:
            response = requests.post(
                f"{self.base_url}/read_file",
                json={'path': path},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'Failed to read file: {str(e)}'}
    
    def write_file(self, path, content):
        try:
            response = requests.post(
                f"{self.base_url}/write_file",
                json={'path': path, 'content': content},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'Failed to write file: {str(e)}'}
    
    def create_script(self, name, parent_path, script_type='Script', content=''):
        try:
            response = requests.post(
                f"{self.base_url}/create_script",
                json={
                    'name': name,
                    'parent_path': parent_path,
                    'script_type': script_type,
                    'content': content
                },
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'Failed to create script: {str(e)}'}
    
    def delete_file(self, path):
        try:
            response = requests.post(
                f"{self.base_url}/delete_file",
                json={'path': path},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'Failed to delete file: {str(e)}'}
    
    def move_file(self, source_path, dest_path):
        try:
            response = requests.post(
                f"{self.base_url}/move_file",
                json={'source_path': source_path, 'dest_path': dest_path},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'Failed to move file: {str(e)}'}
    
    def get_roblox_objects(self, path=''):
        try:
            response = requests.post(
                f"{self.base_url}/get_roblox_objects",
                json={'path': path},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'Failed to get roblox objects: {str(e)}', 'objects': []}
    
    def create_roblox_objects(self, parent_path, object_type, name, properties=None):
        try:
            url = f"{self.base_url}/create_roblox_objects"
            payload = {
                'parent_path': parent_path,
                'object_type': object_type,
                'name': name,
                'properties': properties or {}
            }
            print(f"🔌 MCP Request: POST {url}")
            print(f"📦 Payload: {payload}")
            
            response = requests.post(url, json=payload, timeout=30)
            
            print(f"📡 Response Status: {response.status_code}")
            print(f"📄 Response: {response.text[:500]}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            error_msg = f'HTTP {e.response.status_code} error: {e.response.text[:200]}'
            print(f"❌ MCP Error: {error_msg}")
            return {'error': error_msg}
        except Exception as e:
            error_msg = f'Failed to create roblox object: {str(e)}'
            print(f"❌ MCP Error: {error_msg}")
            return {'error': error_msg}
    
    def modify_object_properties(self, path, properties):
        try:
            response = requests.post(
                f"{self.base_url}/modify_object_properties",
                json={'path': path, 'properties': properties},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'Failed to modify object properties: {str(e)}'}
