#!/usr/bin/env python3
import requests
import json
import os
import time

class MCPController:
    def __init__(self, base_url='http://localhost:3002'):
        self.base_url = base_url
        self.headers = {'ngrok-skip-browser-warning': 'true'}
    
    def check_connection(self):
        try:
            response = requests.get(f"{self.base_url}/health", headers=self.headers, timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def get_file_tree(self):
        response = requests.post(
            f"{self.base_url}/mcp/get_file_tree",
            json={},
            headers=self.headers,
            timeout=10
        )
        return response.json()
    
    def delete_object(self, path):
        response = requests.post(
            f"{self.base_url}/mcp/delete_object",
            json={'path': path},
            headers=self.headers,
            timeout=10
        )
        return response.json()
    
    def create_part(self, name, parent_path, position, size, color=None, material=None):
        properties = {
            'Position': {'X': position[0], 'Y': position[1], 'Z': position[2]},
            'Size': {'X': size[0], 'Y': size[1], 'Z': size[2]},
            'Anchored': True
        }
        if color:
            properties['BrickColor'] = color
        if material:
            properties['Material'] = material
        
        response = requests.post(
            f"{self.base_url}/mcp/create_object_with_properties",
            json={
                'className': 'Part',
                'parent': parent_path,
                'name': name,
                'properties': properties
            },
            headers=self.headers,
            timeout=30
        )
        return response.json()
    
    def create_script(self, name, parent_path, script_type, source):
        properties = {'Source': source}
        response = requests.post(
            f"{self.base_url}/mcp/create_object_with_properties",
            json={
                'className': script_type,
                'parent': parent_path,
                'name': name,
                'properties': properties
            },
            headers=self.headers,
            timeout=30
        )
        return response.json()
    
    def create_folder(self, name, parent_path):
        response = requests.post(
            f"{self.base_url}/mcp/create_object",
            json={
                'class_name': 'Folder',
                'parent_path': parent_path,
                'name': name
            },
            headers=self.headers,
            timeout=10
        )
        return response.json()

def main():
    mcp = MCPController()
    
    print("🔌 Connecting to MCP Server...")
    if not mcp.check_connection():
        print("❌ MCP Server not connected. Make sure:")
        print("   1. RoboVibeCode app is running")
        print("   2. Roblox Studio plugin is active")
        print("   3. MCP server shows 'Connected' status")
        return
    
    print("✅ Connected to MCP Server!")
    
    # Get current project structure
    print("\n📂 Getting current project structure...")
    tree = mcp.get_file_tree()
    print(json.dumps(tree, indent=2))
    
    print("\n🧹 Cleaning workspace...")
    # We'll identify and delete test objects in the next step
    
    print("\n🏗️ Building 10-level high-difficulty obby...")
    
    # Create Workspace folder for the obby
    print("Creating Obby folder...")
    mcp.create_folder("HighDifficultyObby", "Workspace")
    
    # Level 1 - Basic warmup
    print("Building Level 1...")
    mcp.create_part("Level1_Start", "Workspace.HighDifficultyObby", [0, 5, 0], [10, 1, 10], "Bright green", "Plastic")
    mcp.create_part("Level1_Platform1", "Workspace.HighDifficultyObby", [0, 5, 15], [8, 1, 8], "Bright blue")
    mcp.create_part("Level1_Platform2", "Workspace.HighDifficultyObby", [0, 7, 25], [6, 1, 6], "Bright blue")
    
    # Level 2 - Narrow jumps
    print("Building Level 2...")
    mcp.create_part("Level2_Platform1", "Workspace.HighDifficultyObby", [0, 9, 35], [4, 1, 4], "Bright yellow")
    mcp.create_part("Level2_Platform2", "Workspace.HighDifficultyObby", [5, 11, 40], [3, 1, 3], "Bright yellow")
    mcp.create_part("Level2_Platform3", "Workspace.HighDifficultyObby", [-5, 13, 45], [3, 1, 3], "Bright yellow")
    
    # Level 3 - Diagonal jumps
    print("Building Level 3...")
    mcp.create_part("Level3_Platform1", "Workspace.HighDifficultyObby", [5, 15, 50], [3, 1, 3], "Bright orange")
    mcp.create_part("Level3_Platform2", "Workspace.HighDifficultyObby", [10, 17, 55], [2.5, 1, 2.5], "Bright orange")
    mcp.create_part("Level3_Platform3", "Workspace.HighDifficultyObby", [15, 19, 60], [2, 1, 2], "Bright orange")
    
    print("✅ Obby structure created!")
    print("\nNext steps will add:")
    print("- Levels 4-10 with increasing difficulty")
    print("- Checkpoint system")
    print("- Kill parts and respawn")
    print("- Victory celebration")

if __name__ == "__main__":
    main()
