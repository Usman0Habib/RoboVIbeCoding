"""
Tool Registry - Complete documentation of all MCP server capabilities
Provides self-documentation for the AI to understand available tools
"""

class MCPToolRegistry:
    """Registry of all 18 MCP tools with parameters, examples, and best practices"""
    
    @staticmethod
    def get_all_tools():
        """Returns complete documentation of all available MCP tools"""
        return {
            # File System Tools
            "get_file_tree": {
                "category": "File System",
                "description": "Get hierarchical tree of all files and folders in the Roblox project",
                "parameters": {},
                "returns": "Tree structure showing all workspace items, services, and hierarchy",
                "use_cases": ["Project analysis", "Understanding structure", "Finding existing assets"],
                "example": "Use when user asks 'show me my project structure' or before creating new items"
            },
            
            "search_files": {
                "category": "File System",
                "description": "Search for files by name or type",
                "parameters": {
                    "query": "Search term (string)",
                    "file_type": "Optional filter: 'Script', 'LocalScript', 'ModuleScript', etc."
                },
                "returns": "List of matching files with paths",
                "use_cases": ["Finding specific scripts", "Locating assets", "Searching by type"],
                "example": "search_files('Checkpoint', file_type='Script')"
            },
            
            # Studio Context Tools
            "get_place_info": {
                "category": "Studio Context",
                "description": "Get information about current place (PlaceId, Name, etc.)",
                "parameters": {},
                "returns": "Place metadata including ID, name, creator info",
                "use_cases": ["Understanding current project", "Getting place details"],
                "example": "Use when user asks about their game/place"
            },
            
            "get_services": {
                "category": "Studio Context",
                "description": "List all Roblox services (Workspace, Players, ReplicatedStorage, etc.)",
                "parameters": {},
                "returns": "Array of available service names",
                "use_cases": ["Understanding available services", "Validating parent paths"],
                "example": "Use before creating objects to know valid parent services"
            },
            
            "search_objects": {
                "category": "Studio Context",
                "description": "Search for objects in the game hierarchy",
                "parameters": {
                    "query": "Search term (string)",
                    "search_type": "'name' or 'class' (default: 'name')"
                },
                "returns": "List of matching objects with paths",
                "use_cases": ["Finding existing objects", "Locating instances by class"],
                "example": "search_objects('SpawnLocation', search_type='class')"
            },
            
            # Instance & Property Tools
            "get_instance_properties": {
                "category": "Properties",
                "description": "Get all properties of a specific instance",
                "parameters": {
                    "path": "Full instance path (e.g., 'Workspace.Part')"
                },
                "returns": "Dictionary of all properties and their current values",
                "use_cases": ["Verifying object state", "Checking positions", "Debugging"],
                "example": "get_instance_properties('Workspace.Baseplate')"
            },
            
            "get_instance_children": {
                "category": "Properties",
                "description": "Get all children of an instance",
                "parameters": {
                    "path": "Full instance path"
                },
                "returns": "List of child objects with names and classes",
                "use_cases": ["Understanding hierarchy", "Finding descendants", "Verifying structure"],
                "example": "get_instance_children('Workspace')"
            },
            
            "search_by_property": {
                "category": "Properties",
                "description": "Find objects with specific property values",
                "parameters": {
                    "property_name": "Name of property to search",
                    "property_value": "Value to match"
                },
                "returns": "List of objects matching the criteria",
                "use_cases": ["Finding all parts with Transparency=0.5", "Locating colored objects"],
                "example": "search_by_property('BrickColor', 'Bright red')"
            },
            
            "get_class_info": {
                "category": "Properties",
                "description": "Get information about a Roblox class (available properties, etc.)",
                "parameters": {
                    "class_name": "Roblox class name (e.g., 'Part', 'Script')"
                },
                "returns": "Class metadata including available properties",
                "use_cases": ["Understanding what properties a class has", "Validating property names"],
                "example": "get_class_info('Part')"
            },
            
            # Property Modification Tools
            "set_property": {
                "category": "Modification",
                "description": "Set a single property on an instance",
                "parameters": {
                    "path": "Full instance path",
                    "property_name": "Name of property to set",
                    "property_value": "New value"
                },
                "returns": "Success/failure status",
                "use_cases": ["Changing individual properties", "Updating positions", "Setting colors"],
                "example": "set_property('Workspace.Part', 'Position', [0, 5, 0])"
            },
            
            "mass_set_property": {
                "category": "Modification",
                "description": "Set same property on multiple instances at once",
                "parameters": {
                    "paths": "Array of instance paths",
                    "property_name": "Name of property to set",
                    "property_value": "New value for all instances"
                },
                "returns": "Success count and any errors",
                "use_cases": ["Bulk property updates", "Making multiple objects the same color", "Mass positioning"],
                "example": "mass_set_property(['Workspace.Part1', 'Workspace.Part2'], 'Transparency', 0.5)"
            },
            
            "mass_get_property": {
                "category": "Properties",
                "description": "Get same property from multiple instances",
                "parameters": {
                    "paths": "Array of instance paths",
                    "property_name": "Name of property to get"
                },
                "returns": "Dictionary mapping paths to property values",
                "use_cases": ["Verifying multiple objects", "Checking positions of many parts"],
                "example": "mass_get_property(['Workspace.Part1', 'Workspace.Part2'], 'Position')"
            },
            
            # Object Creation Tools
            "create_object": {
                "category": "Creation",
                "description": "Create a single Roblox instance",
                "parameters": {
                    "class_name": "Roblox class (e.g., 'Part', 'Folder')",
                    "parent_path": "Where to create it (e.g., 'Workspace')",
                    "name": "Optional custom name"
                },
                "returns": "Created object path and details",
                "use_cases": ["Creating simple objects", "Making folders", "Basic instantiation"],
                "example": "create_object('Part', 'Workspace', 'MyPart')"
            },
            
            "create_object_with_properties": {
                "category": "Creation",
                "description": "Create an instance and set properties in one call (PREFERRED for objects)",
                "parameters": {
                    "className": "Roblox class name",
                    "parent": "Parent path",
                    "name": "Optional name",
                    "properties": "Dictionary of properties to set"
                },
                "returns": "Created object with properties applied",
                "use_cases": ["Creating positioned objects", "Making parts with specific CFrame/Size", "Setting initial state"],
                "example": "create_object_with_properties('Part', 'Workspace', 'Platform1', {'CFrame': [0, 1, 0], 'Size': [10, 1, 10], 'BrickColor': 'Bright blue'})",
                "best_practice": "ALWAYS use this instead of create_object + set_property for efficiency"
            },
            
            "mass_create_objects_with_properties": {
                "category": "Creation",
                "description": "Create multiple objects with properties in bulk (BEST for obbies, maps, levels)",
                "parameters": {
                    "objects": "Array of object definitions with className, parent, name, properties"
                },
                "returns": "Array of created object details",
                "use_cases": ["Creating obby platforms", "Building maps", "Mass object placement"],
                "example": """mass_create_objects_with_properties([
                    {'className': 'Part', 'parent': 'Workspace', 'name': 'Platform1', 'properties': {'CFrame': [0, 1, 0], 'Size': [10, 1, 10]}},
                    {'className': 'Part', 'parent': 'Workspace', 'name': 'Platform2', 'properties': {'CFrame': [0, 5, 10], 'Size': [10, 1, 10]}}
                ])""",
                "best_practice": "USE THIS for creating multiple objects - it's atomic and much faster"
            },
            
            "delete_object": {
                "category": "Modification",
                "description": "Delete an instance from the game",
                "parameters": {
                    "path": "Full instance path to delete"
                },
                "returns": "Success/failure status",
                "use_cases": ["Removing objects", "Cleanup", "Correcting mistakes"],
                "example": "delete_object('Workspace.OldPart')"
            },
            
            # Script Management Tools
            "get_script_source": {
                "category": "Scripts",
                "description": "Read the source code of a script",
                "parameters": {
                    "instancePath": "Path to script (e.g., 'ServerScriptService.MainScript')"
                },
                "returns": "Source code as text",
                "use_cases": ["Reading existing scripts", "Analyzing code", "Before editing"],
                "example": "get_script_source('ServerScriptService.GameManager')"
            },
            
            "set_script_source": {
                "category": "Scripts",
                "description": "Update the source code of an existing script",
                "parameters": {
                    "instancePath": "Path to script",
                    "source": "New Lua source code"
                },
                "returns": "Success/failure status",
                "use_cases": ["Editing scripts", "Updating code", "Fixing bugs"],
                "example": "set_script_source('ServerScriptService.MainScript', 'print(\"Hello World\")')",
                "best_practice": "Always read the script first with get_script_source before editing"
            },
            
            # Project Analysis Tools
            "get_project_structure": {
                "category": "Analysis",
                "description": "Get detailed analysis of project structure with depth control",
                "parameters": {
                    "depth": "How many levels deep to analyze (default: 5)"
                },
                "returns": "Comprehensive structure analysis",
                "use_cases": ["Deep project analysis", "Understanding complex hierarchies"],
                "example": "get_project_structure(depth=3)"
            }
        }
    
    @staticmethod
    def get_tool_by_category():
        """Organize tools by category for easier discovery"""
        tools = MCPToolRegistry.get_all_tools()
        by_category = {}
        for tool_name, tool_info in tools.items():
            category = tool_info['category']
            if category not in by_category:
                by_category[category] = {}
            by_category[category][tool_name] = tool_info
        return by_category
    
    @staticmethod
    def get_tools_for_task(task_description):
        """Recommend tools based on task description"""
        task_lower = task_description.lower()
        recommendations = []
        
        # Spatial object creation
        if any(word in task_lower for word in ['obby', 'platform', 'map', 'level', 'create multiple']):
            recommendations.append({
                'tool': 'mass_create_objects_with_properties',
                'reason': 'Best for creating multiple positioned objects efficiently',
                'priority': 'HIGH'
            })
        
        # Single object creation
        if 'create' in task_lower and 'object' in task_lower:
            recommendations.append({
                'tool': 'create_object_with_properties',
                'reason': 'Create objects with properties set atomically',
                'priority': 'HIGH'
            })
        
        # Script operations
        if any(word in task_lower for word in ['script', 'code', 'write', 'lua']):
            recommendations.append({
                'tool': 'create_object_with_properties',
                'reason': 'Create scripts with Source property containing code',
                'priority': 'HIGH'
            })
            if 'edit' in task_lower or 'update' in task_lower:
                recommendations.append({
                    'tool': 'get_script_source',
                    'reason': 'Read existing code before editing',
                    'priority': 'CRITICAL'
                })
                recommendations.append({
                    'tool': 'set_script_source',
                    'reason': 'Update script code',
                    'priority': 'HIGH'
                })
        
        # Verification/analysis
        if any(word in task_lower for word in ['check', 'verify', 'analyze', 'show']):
            recommendations.append({
                'tool': 'get_instance_properties',
                'reason': 'Verify object state and properties',
                'priority': 'MEDIUM'
            })
        
        return recommendations
    
    @staticmethod
    def get_tool_documentation(tool_name):
        """Get detailed documentation for a specific tool"""
        tools = MCPToolRegistry.get_all_tools()
        return tools.get(tool_name, None)
    
    @staticmethod
    def generate_tool_context_for_ai():
        """Generate comprehensive tool documentation for AI context"""
        tools = MCPToolRegistry.get_all_tools()
        
        context = """# Complete MCP Tool Reference
You have access to 18 powerful tools for Roblox Studio automation.

## Key Best Practices:
1. ALWAYS use mass_create_objects_with_properties for creating multiple objects (obbies, maps, etc.)
2. ALWAYS use create_object_with_properties instead of create_object + set_property
3. ALWAYS calculate proper CFrame values for spatial positioning - objects need Vector3 positions!
4. ALWAYS verify your work with get_instance_properties after creation
5. For scripts, use create_object_with_properties with Source property set to Lua code

## Tool Categories and Complete Reference:

"""
        
        by_category = MCPToolRegistry.get_tool_by_category()
        for category, tools_in_category in by_category.items():
            context += f"\n### {category} Tools\n\n"
            for tool_name, tool_info in tools_in_category.items():
                context += f"**{tool_name}**\n"
                context += f"- Description: {tool_info['description']}\n"
                if tool_info['parameters']:
                    context += f"- Parameters: {tool_info['parameters']}\n"
                context += f"- Use Cases: {', '.join(tool_info['use_cases'])}\n"
                if 'best_practice' in tool_info:
                    context += f"- ⚠️ BEST PRACTICE: {tool_info['best_practice']}\n"
                context += f"- Example: {tool_info['example']}\n\n"
        
        return context
