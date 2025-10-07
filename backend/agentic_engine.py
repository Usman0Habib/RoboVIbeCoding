import json
import re
from roblox_knowledge import get_roblox_context, get_template, generate_roblox_structure_suggestion

class AgenticEngine:
    def __init__(self, mcp_client, gemini_client, file_manager):
        self.mcp = mcp_client
        self.gemini = gemini_client
        self.file_manager = file_manager
        self.context_history = {}
    
    def process_message(self, user_message, conversation_id):
        if conversation_id not in self.context_history:
            self.context_history[conversation_id] = []
        
        self.context_history[conversation_id].append({
            'role': 'user',
            'content': user_message
        })
        
        context = self._build_context(conversation_id, user_message)
        
        task_plan = self._create_task_plan(user_message, context)
        
        execution_results = []
        for task in task_plan:
            result = self._execute_task(task)
            execution_results.append(result)
        
        response = self._generate_response(user_message, context, task_plan, execution_results)
        
        self.context_history[conversation_id].append({
            'role': 'assistant',
            'content': response
        })
        
        return response
    
    def process_message_stream(self, user_message, conversation_id):
        if conversation_id not in self.context_history:
            self.context_history[conversation_id] = []
        
        self.context_history[conversation_id].append({
            'role': 'user',
            'content': user_message
        })
        
        context = self._build_context(conversation_id, user_message)
        
        yield "🤖 Analyzing request...\n\n"
        
        task_plan = self._create_task_plan(user_message, context)
        
        if task_plan:
            yield f"📋 **Plan:**\n"
            for i, task in enumerate(task_plan, 1):
                yield f"{i}. {task['description']}\n"
            yield "\n"
        
        yield "⚙️ **Executing:**\n\n"
        
        execution_results = []
        for i, task in enumerate(task_plan, 1):
            yield f"▶️ Step {i}: {task['description']}\n"
            result = self._execute_task(task)
            execution_results.append(result)
            
            if result.get('success'):
                yield f"✅ Completed\n\n"
            else:
                yield f"❌ Error: {result.get('error', 'Unknown error')}\n\n"
        
        yield "💭 **Result:**\n\n"
        
        full_prompt = self._create_response_prompt(user_message, context, task_plan, execution_results)
        
        response_text = ""
        for chunk in self.gemini.generate_response_stream(full_prompt):
            response_text += chunk
            yield chunk
        
        self.context_history[conversation_id].append({
            'role': 'assistant',
            'content': response_text
        })
    
    def _build_context(self, conversation_id, user_message):
        context_parts = [get_roblox_context()]
        
        mcp_status = self.mcp.check_connection()
        context_parts.append(f"\nMCP Server Status: {'Connected' if mcp_status else 'Disconnected'}")
        
        if mcp_status:
            if any(keyword in user_message.lower() for keyword in ['analyze', 'project', 'structure', 'file', 'show']):
                tree = self.mcp.get_file_tree()
                if not tree.get('error'):
                    context_parts.append(f"\nCurrent Project Structure:\n{json.dumps(tree, indent=2)}")
        
        history = self.context_history.get(conversation_id, [])[-5:]
        if history:
            context_parts.append("\nRecent Conversation:")
            for msg in history:
                context_parts.append(f"{msg['role']}: {msg['content'][:200]}")
        
        return "\n".join(context_parts)
    
    def _create_task_plan(self, user_message, context):
        tasks = []
        
        msg_lower = user_message.lower()
        
        if 'create script' in msg_lower or 'add script' in msg_lower or 'new script' in msg_lower:
            tasks.append({
                'type': 'create_script',
                'description': 'Create new script in Roblox Studio',
                'params': self._extract_script_params(user_message)
            })
        
        if 'read' in msg_lower or 'show' in msg_lower or 'get' in msg_lower:
            if 'file' in msg_lower or 'script' in msg_lower:
                tasks.append({
                    'type': 'read_file',
                    'description': 'Read file content from Roblox Studio',
                    'params': self._extract_file_path(user_message)
                })
            elif 'structure' in msg_lower or 'tree' in msg_lower or 'project' in msg_lower:
                tasks.append({
                    'type': 'get_file_tree',
                    'description': 'Analyze project structure',
                    'params': {}
                })
        
        if 'write' in msg_lower or 'update' in msg_lower or 'modify' in msg_lower or 'edit' in msg_lower:
            tasks.append({
                'type': 'write_file',
                'description': 'Update file content in Roblox Studio',
                'params': self._extract_write_params(user_message)
            })
        
        if 'create object' in msg_lower or 'add object' in msg_lower or 'new object' in msg_lower:
            tasks.append({
                'type': 'create_object',
                'description': 'Create new Roblox object',
                'params': self._extract_object_params(user_message)
            })
        
        if any(game_type in msg_lower for game_type in ['obby', 'tycoon', 'rpg', 'simulator']):
            tasks.append({
                'type': 'generate_game',
                'description': 'Generate complete game structure',
                'params': {'game_type': self._extract_game_type(user_message)}
            })
        
        if 'backup' in msg_lower or 'save snapshot' in msg_lower:
            tasks.append({
                'type': 'create_backup',
                'description': 'Create project backup',
                'params': {}
            })
        
        if not tasks:
            tasks.append({
                'type': 'chat',
                'description': 'Respond to user query',
                'params': {}
            })
        
        return tasks
    
    def _execute_task(self, task):
        task_type = task['type']
        params = task['params']
        
        try:
            if task_type == 'create_script':
                return self.mcp.create_script(**params)
            
            elif task_type == 'read_file':
                return self.mcp.read_file(params.get('path', ''))
            
            elif task_type == 'write_file':
                return self.mcp.write_file(params.get('path', ''), params.get('content', ''))
            
            elif task_type == 'get_file_tree':
                return self.mcp.get_file_tree()
            
            elif task_type == 'create_object':
                return self.mcp.create_roblox_objects(**params)
            
            elif task_type == 'generate_game':
                return self._generate_game_structure(params.get('game_type', ''))
            
            elif task_type == 'create_backup':
                backup_path = self.file_manager.create_backup()
                return {'success': True, 'backup_path': backup_path}
            
            elif task_type == 'chat':
                return {'success': True, 'type': 'chat'}
            
            else:
                return {'error': f'Unknown task type: {task_type}'}
        
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    def _generate_response(self, user_message, context, task_plan, execution_results):
        prompt = self._create_response_prompt(user_message, context, task_plan, execution_results)
        return self.gemini.generate_response(prompt)
    
    def _create_response_prompt(self, user_message, context, task_plan, execution_results):
        prompt = f"{context}\n\nUser Request: {user_message}\n\n"
        
        if task_plan:
            prompt += "Tasks Executed:\n"
            for i, (task, result) in enumerate(zip(task_plan, execution_results), 1):
                prompt += f"{i}. {task['description']}: "
                if result.get('success'):
                    prompt += "✅ Success"
                    if result.get('content'):
                        prompt += f"\n   Content: {str(result.get('content'))[:500]}"
                else:
                    prompt += f"❌ Error - {result.get('error', 'Unknown')}"
                prompt += "\n"
        
        prompt += "\nProvide a helpful, detailed response to the user. If code was generated or tasks were executed, explain what was done and what the user can expect."
        
        return prompt
    
    def _extract_script_params(self, message):
        name_match = re.search(r'(?:named?|called)\s+["\']?(\w+)["\']?', message, re.IGNORECASE)
        name = name_match.group(1) if name_match else 'NewScript'
        
        script_type = 'Script'
        if 'localscript' in message.lower():
            script_type = 'LocalScript'
        elif 'modulescript' in message.lower():
            script_type = 'ModuleScript'
        
        parent_path = 'ServerScriptService'
        if 'startergui' in message.lower():
            parent_path = 'StarterGui'
        elif 'starterplayer' in message.lower():
            parent_path = 'StarterPlayer/StarterPlayerScripts'
        elif 'replicatedstorage' in message.lower():
            parent_path = 'ReplicatedStorage'
        
        return {
            'name': name,
            'parent_path': parent_path,
            'script_type': script_type,
            'content': ''
        }
    
    def _extract_file_path(self, message):
        path_match = re.search(r'["\']([^"\']+)["\']', message)
        return {'path': path_match.group(1) if path_match else ''}
    
    def _extract_write_params(self, message):
        path_match = re.search(r'["\']([^"\']+)["\']', message)
        return {
            'path': path_match.group(1) if path_match else '',
            'content': ''
        }
    
    def _extract_object_params(self, message):
        name_match = re.search(r'(?:named?|called)\s+["\']?(\w+)["\']?', message, re.IGNORECASE)
        type_match = re.search(r'(?:type|object)\s+["\']?(\w+)["\']?', message, re.IGNORECASE)
        
        return {
            'parent_path': 'Workspace',
            'object_type': type_match.group(1) if type_match else 'Part',
            'name': name_match.group(1) if name_match else 'NewObject',
            'properties': {}
        }
    
    def _extract_game_type(self, message):
        msg_lower = message.lower()
        if 'obby' in msg_lower:
            return 'obby'
        elif 'tycoon' in msg_lower:
            return 'tycoon'
        elif 'rpg' in msg_lower:
            return 'rpg'
        elif 'simulator' in msg_lower:
            return 'simulator'
        return 'generic'
    
    def _generate_game_structure(self, game_type):
        structure = generate_roblox_structure_suggestion(game_type)
        if structure:
            return {
                'success': True,
                'game_type': game_type,
                'structure': structure,
                'message': f'Generated {game_type} game structure with folders and scripts'
            }
        return {
            'success': False,
            'error': f'Unknown game type: {game_type}'
        }
