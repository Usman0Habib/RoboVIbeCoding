import requests
import json

class MCPClient:
    def __init__(self, base_url='http://localhost:3002'):
        self.base_url = base_url
        self.connected = False
        self.headers = {'ngrok-skip-browser-warning': 'true'}
    
    def check_connection(self):
        try:
            response = requests.get(f"{self.base_url}/health", headers=self.headers, timeout=2)
            self.connected = response.status_code == 200
            return self.connected
        except:
            self.connected = False
            return False
    
    # File System Tools
    def get_file_tree(self):
        try:
            response = requests.post(
                f"{self.base_url}/mcp/get_file_tree",
                json={},
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'Failed to get file tree: {str(e)}', 'tree': []}
    
    def search_files(self, query, file_type=None):
        try:
            response = requests.post(
                f"{self.base_url}/mcp/search_files",
                json={'query': query, 'file_type': file_type},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'Failed to search files: {str(e)}'}
    
    # Studio Context Tools
    def get_place_info(self):
        try:
            response = requests.post(
                f"{self.base_url}/mcp/get_place_info",
                json={},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'Failed to get place info: {str(e)}'}
    
    def get_services(self):
        try:
            response = requests.post(
                f"{self.base_url}/mcp/get_services",
                json={},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'Failed to get services: {str(e)}'}
    
    def search_objects(self, query, search_type='name'):
        try:
            response = requests.post(
                f"{self.base_url}/mcp/search_objects",
                json={'query': query, 'search_type': search_type},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'Failed to search objects: {str(e)}'}
    
    # Instance & Property Tools
    def get_instance_properties(self, path):
        try:
            response = requests.post(
                f"{self.base_url}/mcp/get_instance_properties",
                json={'path': path},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'Failed to get instance properties: {str(e)}'}
    
    def get_instance_children(self, path):
        try:
            response = requests.post(
                f"{self.base_url}/mcp/get_instance_children",
                json={'path': path},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'Failed to get instance children: {str(e)}'}
    
    def search_by_property(self, property_name, property_value):
        try:
            response = requests.post(
                f"{self.base_url}/mcp/search_by_property",
                json={'property_name': property_name, 'property_value': property_value},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'Failed to search by property: {str(e)}'}
    
    def get_class_info(self, class_name):
        try:
            response = requests.post(
                f"{self.base_url}/mcp/get_class_info",
                json={'class_name': class_name},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'Failed to get class info: {str(e)}'}
    
    # Property Modification Tools
    def set_property(self, path, property_name, property_value):
        try:
            response = requests.post(
                f"{self.base_url}/mcp/set_property",
                json={'path': path, 'property_name': property_name, 'property_value': property_value},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'Failed to set property: {str(e)}'}
    
    def mass_set_property(self, paths, property_name, property_value):
        try:
            response = requests.post(
                f"{self.base_url}/mcp/mass_set_property",
                json={'paths': paths, 'property_name': property_name, 'property_value': property_value},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'Failed to mass set property: {str(e)}'}
    
    def mass_get_property(self, paths, property_name):
        try:
            response = requests.post(
                f"{self.base_url}/mcp/mass_get_property",
                json={'paths': paths, 'property_name': property_name},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'Failed to mass get property: {str(e)}'}
    
    # Object Creation Tools
    def create_object(self, class_name, parent_path, name=None):
        try:
            payload = {'class_name': class_name, 'parent_path': parent_path}
            if name:
                payload['name'] = name
            
            response = requests.post(
                f"{self.base_url}/mcp/create_object",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'Failed to create object: {str(e)}'}
    
    def create_object_with_properties(self, class_name, parent_path, name=None, properties=None):
        try:
            payload = {
                'className': class_name,
                'parent': parent_path
            }
            if name:
                payload['name'] = name
            if properties:
                payload['properties'] = properties
            
            response = requests.post(
                f"{self.base_url}/mcp/create_object_with_properties",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'Failed to create object with properties: {str(e)}'}
    
    def mass_create_objects(self, objects_data):
        try:
            response = requests.post(
                f"{self.base_url}/mcp/mass_create_objects",
                json={'objects': objects_data},
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'Failed to mass create objects: {str(e)}'}
    
    def mass_create_objects_with_properties(self, objects_data):
        try:
            response = requests.post(
                f"{self.base_url}/mcp/mass_create_objects_with_properties",
                json={'objects': objects_data},
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'Failed to mass create objects with properties: {str(e)}'}
    
    def delete_object(self, path):
        try:
            response = requests.post(
                f"{self.base_url}/mcp/delete_object",
                json={'path': path},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'Failed to delete object: {str(e)}'}
    
    # Project Analysis Tools
    def get_project_structure(self, depth=5):
        try:
            response = requests.post(
                f"{self.base_url}/mcp/get_project_structure",
                json={'depth': depth},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'Failed to get project structure: {str(e)}'}
    
    # Script Management Tools
    def get_script_source(self, instance_path):
        """Get the source code of a script"""
        try:
            response = requests.post(
                f"{self.base_url}/mcp/get_script_source",
                json={'instancePath': instance_path},
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'Failed to get script source: {str(e)}'}
    
    def set_script_source(self, instance_path, source):
        """Set the source code of a script"""
        try:
            response = requests.post(
                f"{self.base_url}/mcp/set_script_source",
                json={'instancePath': instance_path, 'source': source},
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f'Failed to set script source: {str(e)}'}
    
    # Legacy method for backward compatibility - now uses create_object
    def create_script(self, name, parent_path, script_type='Script', content=''):
        """Create a script using create_object_with_properties"""
        properties = {}
        if content:
            properties['Source'] = content
        
        result = self.create_object_with_properties(
            class_name=script_type,
            parent_path=parent_path,
            name=name,
            properties=properties
        )
        
        return result
    
    def call_tool(self, tool_name, params):
        """Generic method to call any MCP tool by name"""
        
        tool_map = {
            'create_object': lambda p: self.create_object(
                p.get('className') or p.get('class_name'),
                p.get('parent') or p.get('parent_path'),
                p.get('name')
            ),
            'create_object_with_properties': lambda p: self.create_object_with_properties(
                p.get('className'), 
                p.get('parent'), 
                p.get('name'), 
                p.get('properties')
            ),
            'mass_create_objects_with_properties': lambda p: self.mass_create_objects_with_properties(
                p.get('objects')
            ),
            'set_property': lambda p: self.set_property(
                p.get('path'),
                p.get('property_name'),
                p.get('property_value')
            ),
            'mass_set_property': lambda p: self.mass_set_property(
                p.get('paths'),
                p.get('property_name'),
                p.get('property_value')
            ),
            'get_instance_properties': lambda p: self.get_instance_properties(p.get('path')),
            'get_instance_children': lambda p: self.get_instance_children(p.get('path')),
            'search_objects': lambda p: self.search_objects(
                p.get('query'),
                p.get('search_type', 'name')
            ),
            'get_file_tree': lambda p: self.get_file_tree(),
            'delete_object': lambda p: self.delete_object(p.get('path')),
            'get_script_source': lambda p: self.get_script_source(p.get('instancePath')),
            'set_script_source': lambda p: self.set_script_source(
                p.get('instancePath'),
                p.get('source')
            ),
        }
        
        if tool_name in tool_map:
            return tool_map[tool_name](params)
        else:
            return {'error': f'Unknown tool: {tool_name}'}
