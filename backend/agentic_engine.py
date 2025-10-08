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
        
        # Check if we can create a direct response without Gemini (for read_script tasks)
        if len(task_plan) == 1 and task_plan[0].get('type') == 'read_script':
            result = execution_results[0]
            if result.get('success') and result.get('content'):
                script_path = task_plan[0]['params'].get('path', 'Unknown')
                response_text = f"Here's the content of `{script_path}`:\n\n```lua\n{result['content']}\n```"
                self.context_history[conversation_id].append({
                    'role': 'assistant',
                    'content': response_text
                })
                yield response_text
                return
            elif result.get('error'):
                response_text = f"❌ Error reading script: {result['error']}\n\nMake sure:\n- The script exists in your Roblox Studio\n- The MCP server is connected\n- The path is correct (e.g., 'ServerScriptService.ScriptName')"
                self.context_history[conversation_id].append({
                    'role': 'assistant',
                    'content': response_text
                })
                yield response_text
                return
        
        # Try to use Gemini for response generation
        try:
            full_prompt = self._create_response_prompt(user_message, context, task_plan, execution_results)
            
            response_text = ""
            for chunk in self.gemini.generate_response_stream(full_prompt):
                response_text += chunk
                yield chunk
            
            self.context_history[conversation_id].append({
                'role': 'assistant',
                'content': response_text
            })
        except Exception as e:
            # Fallback response if Gemini fails
            error_msg = str(e)
            if 'quota' in error_msg.lower() or '429' in error_msg:
                fallback_response = "⚠️ Gemini API quota exceeded. "
            else:
                fallback_response = f"⚠️ Error generating response: {error_msg}\n\n"
            
            # Still show execution results
            if execution_results:
                fallback_response += "\n**Task Results:**\n"
                for i, (task, result) in enumerate(zip(task_plan, execution_results), 1):
                    fallback_response += f"\n{i}. {task['description']}: "
                    if result.get('success'):
                        fallback_response += "✅ Success"
                        if task.get('type') == 'read_script' and result.get('content'):
                            fallback_response += f"\n\n```lua\n{result.get('content')}\n```\n"
                        elif result.get('message'):
                            fallback_response += f" - {result.get('message')}"
                    else:
                        fallback_response += f"❌ {result.get('error', 'Unknown error')}"
            
            self.context_history[conversation_id].append({
                'role': 'assistant',
                'content': fallback_response
            })
            yield fallback_response
    
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
        msg_lower = user_message.lower()
        
        if 'backup' in msg_lower or 'save snapshot' in msg_lower:
            return [{
                'type': 'create_backup',
                'description': 'Create project backup',
                'params': {}
            }]
        
        if 'structure' in msg_lower or 'tree' in msg_lower or 'project' in msg_lower:
            if 'show' in msg_lower or 'get' in msg_lower or 'analyze' in msg_lower:
                return [{
                    'type': 'get_file_tree',
                    'description': 'Analyze project structure',
                    'params': {}
                }]
        
        # Detect script read requests (show/display/read + script path)
        read_keywords = ['show', 'display', 'read', 'get', 'see', 'view', 'content', 'code']
        script_indicators = ['script', 'serverscriptservice', 'localscript', 'modulescript', 'replicatedstorage']
        
        if any(keyword in msg_lower for keyword in read_keywords):
            # Look for script path patterns like "game.ServerScriptService.OrbitHandle" or "ServerScriptService.MyScript"
            import re
            path_patterns = [
                r'game\.([A-Za-z0-9.]+)',  # game.ServerScriptService.ScriptName
                r'(?:^|\s)([A-Za-z0-9]+(?:\.[A-Za-z0-9]+)+)',  # ServerScriptService.ScriptName
            ]
            
            for pattern in path_patterns:
                matches = re.findall(pattern, user_message)
                for match in matches:
                    # Clean up the path (remove "game." prefix if present)
                    path = match.replace('game.', '')
                    
                    # Check if this looks like a script path
                    if any(indicator in path.lower() for indicator in script_indicators):
                        return [{
                            'type': 'read_script',
                            'description': f'Read script content from {path}',
                            'params': {'path': path}
                        }]
        
        planning_prompt = f"""You are an autonomous Roblox development agent. Analyze the request and create a concrete action plan.

User Request: {user_message}

Context: {context[:500]}

Available Actions:
1. create_script - Create new Lua script with code
   Required params: name (string), parent_path (string), script_type ("Script"|"LocalScript"|"ModuleScript"), content (Lua code string)

2. write_file - Update existing file
   Required params: path (string), content (string)

3. create_roblox_objects - Create Roblox objects
   Required params: parent_path (string), object_type (string), name (string), properties (object)

4. read_script - Read script source code
   Required params: path (string - full instance path like "ServerScriptService.MyScript")

5. generate_game - Generate complete game template
   Required params: game_type ("obby"|"tycoon"|"rpg"|"simulator")

6. chat - Simple conversation (use when request is question/discussion)
   Required params: {{}}

CRITICAL: Return ONLY a valid JSON array, no other text before or after.

Example output for "Create a checkpoint system":
[
  {{"type": "create_script", "description": "Create checkpoint manager", "params": {{"name": "CheckpointManager", "parent_path": "ServerScriptService", "script_type": "Script", "content": "local Players = game:GetService(\\"Players\\")\\n\\nPlayers.PlayerAdded:Connect(function(player)\\n    print('Player joined:', player.Name)\\nend)"}}}},
  {{"type": "create_roblox_objects", "description": "Create checkpoints folder", "params": {{"parent_path": "ReplicatedStorage", "object_type": "Folder", "name": "Checkpoints", "properties": {{}}}}}}
]

Now analyze the user request and return the JSON array:"""

        max_retries = 3
        for attempt in range(max_retries):
            try:
                ai_plan = self.gemini.generate_response(planning_prompt)
                print(f"AI response (attempt {attempt + 1}): {ai_plan[:200]}...")
                
                tasks = self._extract_and_validate_tasks(ai_plan)
                
                if tasks:
                    print(f"✅ AI planning successful: {len(tasks)} tasks generated")
                    return tasks
                else:
                    print(f"❌ No valid tasks on attempt {attempt + 1}")
                    if attempt < max_retries - 1:
                        planning_prompt = f"{planning_prompt}\n\nPREVIOUS ATTEMPT FAILED. You must return a valid JSON array with tasks. Example: [{{'type':'create_script','description':'desc','params':{{'name':'Test'}}}}]"
                
            except Exception as e:
                print(f"❌ Planning error on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    planning_prompt = f"{planning_prompt}\n\nERROR: {str(e)}. Return valid JSON array only."
        
        print("⚠️ All planning attempts failed, using chat fallback")
        return [{'type': 'chat', 'description': 'Respond to user query', 'params': {}}]
    
    def _extract_and_validate_tasks(self, ai_response):
        """Extract and validate task list from AI response with multiple strategies"""
        ai_response = ai_response.strip()
        
        strategies = [
            lambda s: s,
            lambda s: s.split('```json')[-1].split('```')[0] if '```json' in s else None,
            lambda s: s.split('```')[-2] if s.count('```') >= 2 else None,
            lambda s: s[s.find('['):s.rfind(']')+1] if '[' in s and ']' in s else None,
        ]
        
        for strategy in strategies:
            try:
                extracted = strategy(ai_response)
                if not extracted:
                    continue
                    
                extracted = extracted.strip()
                if not extracted:
                    continue
                
                tasks = json.loads(extracted)
                
                if not isinstance(tasks, list):
                    continue
                
                if len(tasks) == 0:
                    continue
                
                valid_tasks = []
                for task in tasks:
                    if not isinstance(task, dict):
                        continue
                    
                    if 'type' not in task or not task['type']:
                        task['type'] = 'chat'
                    
                    if 'params' not in task or not isinstance(task['params'], dict):
                        task['params'] = {}
                    
                    if 'description' not in task or not task['description']:
                        task['description'] = f"Execute {task['type']}"
                    
                    task_type = task['type']
                    params = task['params']
                    
                    if task_type == 'create_script':
                        params.setdefault('name', 'NewScript')
                        params.setdefault('parent_path', 'ServerScriptService')
                        params.setdefault('script_type', 'Script')
                        params.setdefault('content', '')
                    
                    elif task_type == 'write_file':
                        if not params.get('path'):
                            print(f"⚠️ write_file missing path, converting to chat")
                            task['type'] = 'chat'
                            task['description'] = 'Unable to write file - missing path parameter. Providing guidance instead.'
                            task['params'] = {'error': 'Missing required path parameter'}
                        else:
                            params.setdefault('content', '')
                    
                    elif task_type in ['create_roblox_objects', 'create_object']:
                        params.setdefault('parent_path', 'Workspace')
                        params.setdefault('object_type', 'Part')
                        params.setdefault('name', 'NewObject')
                        params.setdefault('properties', {})
                    
                    elif task_type in ['read_file', 'read_script']:
                        if not params.get('path'):
                            print(f"⚠️ read_script missing path, converting to chat")
                            task['type'] = 'chat'
                            task['description'] = 'Unable to read script - missing path parameter. Providing guidance instead.'
                            task['params'] = {'error': 'Missing required path parameter'}
                    
                    elif task_type == 'generate_game':
                        params.setdefault('game_type', 'generic')
                    
                    valid_tasks.append(task)
                
                if valid_tasks:
                    return valid_tasks
                    
            except json.JSONDecodeError:
                continue
            except Exception:
                continue
        
        return None
    
    def _execute_task(self, task):
        task_type = task.get('type', 'chat')
        params = task.get('params', {})
        
        try:
            if task_type == 'create_script':
                name = params.get('name', 'NewScript')
                parent_path = params.get('parent_path', 'ServerScriptService')
                script_type = params.get('script_type', 'Script')
                content = params.get('content', '')
                
                result = self.mcp.create_script(name, parent_path, script_type, content)
                
                if result.get('error'):
                    return {'success': False, 'error': result.get('error')}
                return {'success': True, 'message': f'Created {script_type} named {name}', 'result': result}
            
            elif task_type == 'read_file' or task_type == 'read_script':
                path = params.get('path', '')
                if not path:
                    return {'success': False, 'error': 'No file path specified'}
                
                result = self.mcp.get_script_source(path)
                if result.get('error'):
                    return {'success': False, 'error': result.get('error')}
                
                source = result.get('content', [{}])[0].get('text', '') if isinstance(result.get('content'), list) else result.get('source', '')
                return {'success': True, 'content': source, 'result': result}
            
            elif task_type == 'write_file':
                path = params.get('path', '')
                content = params.get('content', '')
                
                if not path:
                    return {'success': False, 'error': 'No file path specified'}
                
                result = self.mcp.write_file(path, content)
                if result.get('error'):
                    return {'success': False, 'error': result.get('error')}
                return {'success': True, 'message': f'Updated file {path}', 'result': result}
            
            elif task_type == 'get_file_tree':
                result = self.mcp.get_file_tree()
                if result.get('error'):
                    return {'success': False, 'error': result.get('error')}
                return {'success': True, 'tree': result.get('tree', []), 'result': result}
            
            elif task_type == 'create_roblox_objects' or task_type == 'create_object':
                object_type = params.get('object_type', 'Part')
                name = params.get('name', 'NewObject')
                properties = params.get('properties', {})
                parent_path = params.get('parent_path', 'Workspace')
                
                result = self.mcp.create_object_with_properties(
                    class_name=object_type,
                    parent_path=parent_path,
                    name=name,
                    properties=properties
                )
                
                if result.get('error'):
                    return {'success': False, 'error': result.get('error')}
                return {'success': True, 'message': f'Created {object_type} named {name}', 'result': result}
            
            elif task_type == 'generate_game':
                return self._generate_game_structure(params.get('game_type', 'generic'))
            
            elif task_type == 'create_backup':
                backup_path = self.file_manager.create_backup()
                return {'success': True, 'backup_path': backup_path, 'message': 'Backup created'}
            
            elif task_type == 'chat':
                if params.get('error'):
                    return {'success': False, 'type': 'chat', 'error': params.get('error'), 'is_fallback': True}
                return {'success': True, 'type': 'chat'}
            
            else:
                return {'success': False, 'error': f'Unknown task type: {task_type}'}
        
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            print(f"Task execution error: {error_detail}")
            return {'success': False, 'error': str(e)}
    
    def _generate_response(self, user_message, context, task_plan, execution_results):
        prompt = self._create_response_prompt(user_message, context, task_plan, execution_results)
        return self.gemini.generate_response(prompt)
    
    def _create_response_prompt(self, user_message, context, task_plan, execution_results):
        prompt = f"{context}\n\nUser Request: {user_message}\n\n"
        
        if task_plan:
            prompt += "Tasks Executed:\n"
            for i, (task, result) in enumerate(zip(task_plan, execution_results), 1):
                prompt += f"{i}. {task['description']}: "
                if result.get('is_fallback'):
                    prompt += f"⚠️ Skipped - {result.get('error', 'Missing required parameters')}"
                elif result.get('success'):
                    prompt += "✅ Success"
                    # For read_script tasks, show FULL content
                    if task.get('type') == 'read_script' and result.get('content'):
                        prompt += f"\n\n=== SCRIPT CONTENT ===\n{result.get('content')}\n=== END SCRIPT ===\n"
                    elif result.get('content'):
                        prompt += f"\n   Content: {str(result.get('content'))[:500]}"
                    if result.get('message'):
                        prompt += f"\n   {result.get('message')}"
                else:
                    prompt += f"❌ Error - {result.get('error', 'Unknown')}"
                prompt += "\n"
        
        prompt += "\nProvide a helpful, detailed response to the user. "
        prompt += "If a script was read, display the ENTIRE script content in a code block (```lua). "
        prompt += "If tasks were skipped due to missing parameters, apologize and ask for the needed information. "
        prompt += "If code was generated or tasks were executed successfully, explain what was done and what the user can expect. "
        prompt += "Be transparent about what worked and what didn't."
        
        return prompt
    
    def _generate_game_structure(self, game_type):
        structure = generate_roblox_structure_suggestion(game_type)
        if not structure:
            return {
                'success': False,
                'error': f'Unknown game type: {game_type}'
            }
        
        created_items = []
        errors = []
        
        for folder_path in structure.get('folders', []):
            try:
                parts = folder_path.split('/')
                parent = '/'.join(parts[:-1]) if len(parts) > 1 else 'Workspace'
                folder_name = parts[-1]
                
                result = self.mcp.create_object(
                    class_name='Folder',
                    parent_path=parent,
                    name=folder_name
                )
                
                if result.get('error'):
                    errors.append(f"Folder {folder_path}: {result.get('error')}")
                else:
                    created_items.append(f"Folder: {folder_path}")
            except Exception as e:
                errors.append(f"Folder {folder_path}: {str(e)}")
        
        for script_path, script_type in structure.get('scripts', []):
            try:
                parts = script_path.split('/')
                parent = '/'.join(parts[:-1])
                script_name = parts[-1]
                
                template_content = get_template('module_script', module_name=script_name, function_name='Init') if script_type == 'ModuleScript' else f'-- {script_name}\nprint("Hello from {script_name}")'
                
                result = self.mcp.create_script(script_name, parent, script_type, template_content)
                if result.get('error'):
                    errors.append(f"Script {script_path}: {result.get('error')}")
                else:
                    created_items.append(f"Script: {script_path} ({script_type})")
            except Exception as e:
                errors.append(f"Script {script_path}: {str(e)}")
        
        return {
            'success': len(created_items) > 0,
            'game_type': game_type,
            'structure': structure,
            'created_items': created_items,
            'errors': errors,
            'message': f'Generated {game_type} game structure: {len(created_items)} items created' + (f', {len(errors)} errors' if errors else '')
        }
