"""
Advanced Planning Engine with Chain-of-Thought Reasoning
Provides sophisticated task decomposition rivaling Replit Agent
"""

import json
from tool_registry import MCPToolRegistry
from spatial_engine import SpatialEngine
from roblox_knowledge import get_property_template

class AdvancedPlanner:
    """
    Multi-level planning system with chain-of-thought reasoning
    Breaks down complex goals into atomic, verifiable, spatially-aware tasks
    """
    
    def __init__(self, gemini_client):
        self.gemini = gemini_client
        self.tool_registry = MCPToolRegistry()
    
    def create_advanced_plan(self, user_request, context):
        """
        Create a sophisticated multi-level plan using chain-of-thought reasoning
        
        Returns: List of atomic tasks with spatial awareness and verification steps
        """
        
        # First, analyze the request with chain-of-thought
        analysis = self._analyze_request_with_cot(user_request, context)
        
        # Then create hierarchical task decomposition
        tasks = self._hierarchical_decomposition(user_request, analysis, context)
        
        return tasks
    
    def _analyze_request_with_cot(self, user_request, context):
        """Chain-of-thought analysis of the user request"""
        
        tool_docs = self.tool_registry.generate_tool_context_for_ai()
        
        cot_prompt = f"""{tool_docs}

# Chain-of-Thought Analysis

User Request: "{user_request}"

Think through this step-by-step:

1. UNDERSTAND THE GOAL
   - What is the user trying to achieve?
   - What type of game/system are they building?
   - What are the key requirements?

2. IDENTIFY COMPONENTS NEEDED
   - What objects need to be created?
   - What scripts are required?
   - What spatial arrangements are needed?

3. SPATIAL REASONING (CRITICAL!)
   - Do objects need specific positions? (If yes, calculate CFrames!)
   - Should objects be arranged in a pattern? (grid, line, circle, etc.)
   - Are there multiple objects that need DIFFERENT positions?
   - Example: Obby platforms MUST have different X/Y/Z coordinates!

4. TOOL SELECTION
   - Which MCP tools are best for each step?
   - Should I use mass_create_objects_with_properties for multiple objects?
   - Do I need verification steps?

5. DEPENDENCY ANALYSIS
   - What must be created first?
   - What depends on what?
   - What can be done in parallel?

6. VERIFICATION STRATEGY
   - How will I verify each step worked?
   - What properties should I check?
   - How do I handle errors?

Provide your analysis in this JSON format:
{{
    "goal": "brief description of what user wants",
    "components": ["component1", "component2", ...],
    "spatial_requirements": {{
        "needs_positioning": true/false,
        "layout_type": "linear/grid/circular/custom/none",
        "num_objects": number,
        "reasoning": "why this layout?"
    }},
    "tool_recommendations": ["tool1", "tool2", ...],
    "dependencies": {{"task": "depends_on_task"}},
    "verification_needs": ["what to verify"]
}}

Return ONLY the JSON, no other text."""

        try:
            analysis_text = self.gemini.generate_response(cot_prompt)
            
            # Extract JSON from response
            analysis = self._extract_json(analysis_text)
            
            if not analysis:
                # Fallback analysis
                analysis = {
                    "goal": user_request,
                    "components": ["unknown"],
                    "spatial_requirements": {"needs_positioning": False, "layout_type": "none", "num_objects": 0},
                    "tool_recommendations": ["create_object_with_properties"],
                    "dependencies": {},
                    "verification_needs": []
                }
            
            return analysis
            
        except Exception as e:
            print(f"CoT analysis error: {e}")
            return {
                "goal": user_request,
                "components": [],
                "spatial_requirements": {"needs_positioning": False, "layout_type": "none"},
                "tool_recommendations": [],
                "dependencies": {},
                "verification_needs": []
            }
    
    def _hierarchical_decomposition(self, user_request, analysis, context):
        """
        Break down the goal into hierarchical tasks with spatial awareness
        """
        
        # Check for common patterns first
        request_lower = user_request.lower()
        
        # OBBY DETECTION AND SMART PLANNING
        if any(word in request_lower for word in ['obby', 'obstacle course', 'parkour']):
            return self._plan_obby(user_request, analysis)
        
        # TYCOON DETECTION
        if 'tycoon' in request_lower:
            return self._plan_tycoon(user_request, analysis)
        
        # BUILDING/MAP DETECTION
        if any(word in request_lower for word in ['build', 'house', 'tower', 'shop', 'map']):
            return self._plan_building(user_request, analysis)
        
        # SCRIPT-ONLY REQUESTS
        if any(word in request_lower for word in ['script', 'code', 'system']) and 'create' in request_lower:
            return self._plan_script_system(user_request, analysis)
        
        # Generic hierarchical planning with AI
        return self._plan_with_ai(user_request, analysis, context)
    
    def _plan_obby(self, user_request, analysis):
        """Specialized planning for obby creation with proper spatial positioning"""
        
        # Extract number of platforms
        import re
        num_match = re.search(r'(\d+)\s*(?:platform|stage|level|part)', user_request.lower())
        num_platforms = int(num_match.group(1)) if num_match else 10
        
        # Extract difficulty
        difficulty = 'medium'
        if 'easy' in user_request.lower():
            difficulty = 'easy'
        elif 'hard' in user_request.lower():
            difficulty = 'hard'
        
        # Use spatial engine to calculate proper positions
        platform_configs = SpatialEngine.calculate_obby_platforms(num_platforms, difficulty)
        
        tasks = []
        
        # Task 1: Create checkpoints folder
        tasks.append({
            'type': 'create_object',
            'description': 'Create Checkpoints folder in Workspace',
            'params': {
                'className': 'Folder',
                'parent': 'game.Workspace',
                'name': 'Checkpoints',
                'properties': {}
            },
            'reasoning': 'Organize checkpoints in dedicated folder',
            'verify_with': 'get_instance_children',
            'verify_params': {'path': 'game.Workspace'}
        })
        
        # Task 2: Create all platforms with PROPER POSITIONING
        tasks.append({
            'type': 'mass_create_objects_with_properties',
            'description': f'Create {num_platforms} obby platforms with calculated positions',
            'params': {
                'objects': platform_configs
            },
            'reasoning': f'Using mass_create for efficiency with spatially calculated positions. Each platform has unique CFrame coordinates for proper spacing.',
            'verify_with': 'get_instance_children',
            'verify_params': {'path': 'Workspace'},
            'verify_condition': f'Check that {num_platforms} platforms exist with different positions'
        })
        
        # Task 3: Create spawn location on first platform
        first_platform_cframe = platform_configs[0]['properties']['CFrame']
        first_platform_size = platform_configs[0]['properties']['Size']
        spawn_cframe = SpatialEngine.get_spawn_location(first_platform_cframe, first_platform_size)
        
        tasks.append({
            'type': 'create_object_with_properties',
            'description': 'Create SpawnLocation on first platform',
            'params': {
                'className': 'SpawnLocation',
                'parent': 'game.Workspace',
                'name': 'StartSpawn',
                'properties': {
                    'CFrame': spawn_cframe,
                    'Size': [6, 1, 6],
                    'BrickColor': 'Bright green',
                    'Transparency': 0,
                    'Duration': 0
                }
            },
            'reasoning': 'Players need a spawn point on the first platform',
            'verify_with': 'get_instance_properties',
            'verify_params': {'path': 'game.Workspace.StartSpawn'}
        })
        
        # Task 4: Move platforms to Checkpoints folder
        tasks.append({
            'type': 'move_to_folder',
            'description': 'Organize platforms into Checkpoints folder',
            'params': {
                'platform_names': [f'Platform{i+1}' for i in range(num_platforms)],
                'folder_path': 'Workspace.Checkpoints'
            },
            'reasoning': 'Keep workspace organized',
            'note': 'This requires manual implementation or script'
        })
        
        # Task 5: Create checkpoint system script
        from roblox_knowledge import get_template
        checkpoint_script = get_template('checkpoint_system')
        
        tasks.append({
            'type': 'create_script',
            'description': 'Create checkpoint system script',
            'params': {
                'name': 'CheckpointSystem',
                'parent_path': 'ServerScriptService',
                'script_type': 'Script',
                'content': checkpoint_script
            },
            'reasoning': 'Script to handle checkpoint saving and respawning',
            'verify_with': 'get_script_source',
            'verify_params': {'instancePath': 'ServerScriptService.CheckpointSystem'}
        })
        
        return tasks
    
    def _plan_tycoon(self, user_request, analysis):
        """Specialized planning for tycoon games"""
        tasks = []
        
        # Folder structure
        tasks.append({
            'type': 'create_object',
            'description': 'Create TycoonData folder',
            'params': {
                'className': 'Folder',
                'parent': 'ReplicatedStorage',
                'name': 'TycoonData',
                'properties': {}
            }
        })
        
        # Base plot
        tasks.append({
            'type': 'create_object_with_properties',
            'description': 'Create tycoon base plot',
            'params': {
                'className': 'Part',
                'parent': 'game.Workspace',
                'name': 'TycoonPlot',
                'properties': {
                    'CFrame': [0, 0.5, 0],
                    'Size': [50, 1, 50],
                    'BrickColor': 'Dark green',
                    'Anchored': True
                }
            }
        })
        
        return tasks
    
    def _plan_building(self, user_request, analysis):
        """Specialized planning for buildings and structures"""
        tasks = []
        
        # Determine building type
        building_type = 'house'
        if 'tower' in user_request.lower():
            building_type = 'tower'
        elif 'shop' in user_request.lower():
            building_type = 'shop'
        
        # Determine size
        size = 'medium'
        if 'small' in user_request.lower():
            size = 'small'
        elif 'large' in user_request.lower() or 'big' in user_request.lower():
            size = 'large'
        
        # Get building configuration from spatial engine
        building_objects = SpatialEngine.calculate_building_layout(building_type, size)
        
        if building_objects:
            tasks.append({
                'type': 'mass_create_objects_with_properties',
                'description': f'Create {building_type} structure ({size})',
                'params': {
                    'objects': building_objects
                },
                'reasoning': f'Using spatial engine to create properly positioned {building_type} components',
                'verify_with': 'get_instance_children',
                'verify_params': {'path': 'Workspace'}
            })
        
        return tasks
    
    def _plan_script_system(self, user_request, analysis):
        """Planning for script-based systems"""
        tasks = []
        
        # Use AI to generate the script content
        script_prompt = f"""Create a Lua script for Roblox that implements: {user_request}

Requirements:
- Follow Roblox best practices
- Use proper service access via game:GetService()
- Include error handling with pcall where appropriate
- Add comments explaining the code
- Make it production-ready

Return ONLY the Lua code, no explanations."""
        
        script_content = self.gemini.generate_response(script_prompt)
        
        # Determine script type and location
        script_type = 'Script'
        parent_path = 'ServerScriptService'
        
        if 'local' in user_request.lower() or 'client' in user_request.lower():
            script_type = 'LocalScript'
            parent_path = 'StarterPlayer.StarterPlayerScripts'
        elif 'module' in user_request.lower():
            script_type = 'ModuleScript'
            parent_path = 'ReplicatedStorage'
        
        # Extract script name from request
        import re
        name_match = re.search(r'(?:called|named)\s+["\']?(\w+)["\']?', user_request)
        script_name = name_match.group(1) if name_match else 'NewScript'
        
        tasks.append({
            'type': 'create_script',
            'description': f'Create {script_type} for {user_request}',
            'params': {
                'name': script_name,
                'parent_path': parent_path,
                'script_type': script_type,
                'content': script_content
            },
            'reasoning': f'Generated complete script based on requirements',
            'verify_with': 'get_script_source',
            'verify_params': {'instancePath': f'{parent_path}.{script_name}'}
        })
        
        return tasks
    
    def _plan_with_ai(self, user_request, analysis, context):
        """Fallback: Use AI for generic planning with tool awareness"""
        
        tool_docs = self.tool_registry.generate_tool_context_for_ai()
        
        planning_prompt = f"""{tool_docs}

Analysis of user request:
{json.dumps(analysis, indent=2)}

User Request: "{user_request}"

Context: {context[:300]}

Create a detailed execution plan. CRITICAL RULES:

1. SPATIAL AWARENESS:
   - If creating multiple objects, they MUST have DIFFERENT CFrame positions!
   - Use mass_create_objects_with_properties with calculated positions
   - Example: Obby platforms need spacing between them (different X, Y, or Z values)

2. TOOL SELECTION:
   - ALWAYS use mass_create_objects_with_properties for multiple objects
   - ALWAYS use create_object_with_properties (never plain create_object)
   - Include verification steps using get_instance_properties

3. TASK FORMAT:
   Each task must have:
   - type: MCP tool name
   - description: what this does
   - params: exact parameters for the tool
   - reasoning: why this approach
   - verify_with: (optional) tool to verify success
   - verify_params: (optional) params for verification

Return ONLY a JSON array of tasks:
[
  {{
    "type": "create_object_with_properties",
    "description": "...",
    "params": {{...}},
    "reasoning": "...",
    "verify_with": "get_instance_properties",
    "verify_params": {{...}}
  }}
]
"""
        
        max_retries = 2
        for attempt in range(max_retries):
            try:
                response = self.gemini.generate_response(planning_prompt)
                tasks = self._extract_json(response)
                
                if tasks and isinstance(tasks, list) and len(tasks) > 0:
                    return tasks
                    
            except Exception as e:
                print(f"AI planning attempt {attempt + 1} failed: {e}")
        
        # Ultimate fallback
        return [{
            'type': 'chat',
            'description': 'Unable to create detailed plan, providing guidance',
            'params': {},
            'reasoning': 'Fallback to chat mode'
        }]
    
    def _extract_json(self, text):
        """Extract JSON from AI response"""
        text = text.strip()
        
        # Try different extraction strategies
        strategies = [
            lambda s: s,
            lambda s: s.split('```json')[-1].split('```')[0] if '```json' in s else None,
            lambda s: s.split('```')[-2] if s.count('```') >= 2 else None,
            lambda s: s[s.find('['):s.rfind(']')+1] if '[' in s and ']' in s else None,
            lambda s: s[s.find('{'):s.rfind('}')+1] if '{' in s and '}' in s else None,
        ]
        
        for strategy in strategies:
            try:
                extracted = strategy(text)
                if extracted:
                    return json.loads(extracted.strip())
            except:
                continue
        
        return None
