"""
Enhanced Agentic Engine - Integrates all advanced AI components
Rivals Replit Agent with chain-of-thought reasoning, spatial awareness, and iterative debugging
"""

import json
import re
from roblox_knowledge import get_roblox_context, get_template, generate_roblox_structure_suggestion
from tool_registry import MCPToolRegistry
from spatial_engine import SpatialEngine
from advanced_planner import AdvancedPlanner
from execution_engine import ExecutionEngine

def format_tree_visual(tree_data, prefix="", is_last=True):
    """Format tree data into a visual tree structure"""
    if not tree_data:
        return "No files found"
    
    lines = []
    
    def add_node(node, prefix="", is_last=True):
        if isinstance(node, dict):
            name = node.get('name', 'Unknown')
            node_type = node.get('type', '')
            children = node.get('children', [])
            
            connector = "└── " if is_last else "├── "
            icon = "📁 " if node_type == 'folder' else "📄 "
            lines.append(f"{prefix}{connector}{icon}{name}")
            
            if children:
                extension = "    " if is_last else "│   "
                for i, child in enumerate(children):
                    add_node(child, prefix + extension, i == len(children) - 1)
        elif isinstance(node, list):
            for i, item in enumerate(node):
                add_node(item, prefix, i == len(node) - 1)
    
    if isinstance(tree_data, dict) and 'tree' in tree_data:
        tree_data = tree_data['tree']
    
    add_node(tree_data)
    return "\n".join(lines)


class EnhancedAgenticEngine:
    """
    Next-generation agentic AI engine with:
    - Chain-of-thought reasoning for complex problem solving
    - Spatial awareness for proper object positioning
    - Comprehensive tool knowledge (all 18 MCP tools)
    - Automatic verification and error recovery
    - Iterative debugging capabilities
    """
    
    def __init__(self, mcp_client, gemini_client, file_manager):
        self.mcp = mcp_client
        self.gemini = gemini_client
        self.file_manager = file_manager
        
        # Initialize enhanced components
        self.tool_registry = MCPToolRegistry()
        self.spatial_engine = SpatialEngine()
        self.planner = AdvancedPlanner(gemini_client)
        self.executor = ExecutionEngine(mcp_client)
        
        self.context_history = {}
    
    def process_message(self, user_message, conversation_id):
        """
        Non-streaming version for API compatibility
        """
        if conversation_id not in self.context_history:
            self.context_history[conversation_id] = []
        
        self.context_history[conversation_id].append({
            'role': 'user',
            'content': user_message
        })
        
        # Build context
        context = self._build_enhanced_context(conversation_id, user_message)
        
        # Handle simple requests
        simple_result = self._handle_simple_requests(user_message)
        if simple_result:
            result = self._execute_simple_task_sync(simple_result)
            self.context_history[conversation_id].append({
                'role': 'assistant',
                'content': result
            })
            return result
        
        # Create plan and execute
        try:
            task_plan = self.planner.create_advanced_plan(user_message, context)
            execution_result = self.executor.execute_plan_with_recovery(task_plan)
            
            # Generate summary
            summary = self._generate_fallback_summary(task_plan, execution_result)
            self.context_history[conversation_id].append({
                'role': 'assistant',
                'content': summary
            })
            return summary
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.context_history[conversation_id].append({
                'role': 'assistant',
                'content': error_msg
            })
            return error_msg
    
    def _execute_simple_task_sync(self, task):
        """Execute simple task synchronously"""
        task_type = task.get('type')
        params = task.get('params', {})
        
        if task_type == 'get_file_tree':
            result = self.mcp.get_file_tree()
            if result.get('error'):
                return f"Error: {result.get('error')}"
            else:
                tree_visual = format_tree_visual(result.get('tree', []))
                return f"Here's your project structure:\n\n```\n{tree_visual}\n```"
        
        elif task_type == 'read_script':
            path = params.get('path', '')
            result = self.mcp.get_script_source(path)
            
            if result.get('error'):
                return f"Error reading script: {result.get('error')}"
            else:
                source = result.get('content', [{}])[0].get('text', '') if isinstance(result.get('content'), list) else result.get('source', '')
                return f"Here's the content of `{path}`:\n\n```lua\n{source}\n```"
        
        return "Task completed"
    
    def process_message_stream(self, user_message, conversation_id):
        """
        Process user message with streaming response using enhanced AI capabilities
        """
        if conversation_id not in self.context_history:
            self.context_history[conversation_id] = []
        
        self.context_history[conversation_id].append({
            'role': 'user',
            'content': user_message
        })
        
        yield "🧠 Analyzing request with advanced AI...\n\n"
        
        # Build rich context
        context = self._build_enhanced_context(conversation_id, user_message)
        
        # Handle simple/direct requests first (no AI planning needed)
        simple_result = self._handle_simple_requests(user_message)
        if simple_result:
            for chunk in self._execute_simple_task_stream(simple_result, user_message, context, conversation_id):
                yield chunk
            return
        
        # Use advanced planner for complex requests
        yield "📊 Creating intelligent plan with spatial awareness...\n\n"
        
        try:
            task_plan = self.planner.create_advanced_plan(user_message, context)
        except Exception as e:
            yield f"⚠️ Planning error: {e}\n\n"
            task_plan = self._fallback_plan(user_message)
        
        if task_plan:
            yield f"📋 **Execution Plan:**\n"
            for i, task in enumerate(task_plan, 1):
                description = task.get('description', 'Unknown task')
                reasoning = task.get('reasoning', '')
                yield f"{i}. {description}\n"
                if reasoning and len(task_plan) <= 5:  # Show reasoning for small plans
                    yield f"   💭 {reasoning[:100]}...\n"
            yield "\n"
        
        yield "⚙️ **Executing with verification:**\n\n"
        
        # Execute plan with automatic verification
        execution_result = self.executor.execute_plan_with_recovery(task_plan)
        
        # Report execution results
        completed = execution_result.get('completed_tasks', 0)
        total = execution_result.get('total_tasks', 0)
        success_rate = (completed / total * 100) if total > 0 else 0
        
        yield f"✅ Completed {completed}/{total} tasks ({success_rate:.0f}% success rate)\n\n"
        
        if execution_result.get('errors'):
            yield "⚠️ **Issues encountered:**\n"
            for error in execution_result['errors']:
                yield f"  - {error.get('task', 'Unknown')}: {error.get('error', 'Unknown error')}\n"
            yield "\n"
        
        # Generate intelligent summary
        yield "💭 **Summary:**\n\n"
        
        try:
            summary_prompt = self._create_summary_prompt(
                user_message, 
                context, 
                task_plan, 
                execution_result
            )
            
            summary_text = ""
            for chunk in self.gemini.generate_response_stream(summary_prompt):
                summary_text += chunk
                yield chunk
            
            self.context_history[conversation_id].append({
                'role': 'assistant',
                'content': summary_text
            })
            
        except Exception as e:
            fallback = self._generate_fallback_summary(task_plan, execution_result)
            yield fallback
            self.context_history[conversation_id].append({
                'role': 'assistant',
                'content': fallback
            })
    
    def _build_enhanced_context(self, conversation_id, user_message):
        """Build rich context with tool documentation and project state"""
        
        context_parts = [get_roblox_context()]
        
        # Add tool registry context
        tool_context = self.tool_registry.generate_tool_context_for_ai()
        context_parts.append(tool_context)
        
        # Add MCP connection status
        mcp_status = self.mcp.check_connection()
        context_parts.append(f"\nMCP Server Status: {'Connected ✓' if mcp_status else 'Disconnected ✗'}")
        
        # Add project structure if relevant
        if mcp_status:
            if any(keyword in user_message.lower() for keyword in ['analyze', 'project', 'structure', 'show', 'obby', 'game']):
                tree = self.mcp.get_file_tree()
                if not tree.get('error'):
                    context_parts.append(f"\nCurrent Project Structure:\n{json.dumps(tree, indent=2)[:500]}")
        
        # Add conversation history
        history = self.context_history.get(conversation_id, [])[-3:]
        if history:
            context_parts.append("\nRecent Context:")
            for msg in history:
                context_parts.append(f"{msg['role']}: {msg['content'][:150]}")
        
        return "\n".join(context_parts)
    
    def _handle_simple_requests(self, user_message):
        """Detect and handle simple requests without complex planning"""
        
        msg_lower = user_message.lower()
        
        # Project structure request
        if any(word in msg_lower for word in ['structure', 'tree', 'show project', 'analyze project']):
            if 'show' in msg_lower or 'get' in msg_lower or 'analyze' in msg_lower or 'what' in msg_lower:
                return {
                    'type': 'get_file_tree',
                    'description': 'Get project structure',
                    'params': {}
                }
        
        # Script read request
        read_keywords = ['show', 'display', 'read', 'get', 'see', 'view', 'content', 'code']
        script_indicators = ['script', 'serverscriptservice', 'localscript', 'modulescript']
        
        if any(keyword in msg_lower for keyword in read_keywords):
            # Extract path
            import re
            path_patterns = [
                r'game\.([A-Za-z0-9.]+)',
                r'(?:^|\s)([A-Za-z0-9]+(?:\.[A-Za-z0-9]+)+)',
            ]
            
            for pattern in path_patterns:
                matches = re.findall(pattern, user_message)
                for match in matches:
                    path = match.replace('game.', '')
                    if any(indicator in path.lower() for indicator in script_indicators):
                        return {
                            'type': 'read_script',
                            'description': f'Read {path}',
                            'params': {'path': path}
                        }
        
        return None
    
    def _execute_simple_task_stream(self, task, user_message, context, conversation_id):
        """Execute simple task and stream response"""
        
        task_type = task.get('type')
        params = task.get('params', {})
        
        yield f"▶️ {task.get('description', 'Processing')}...\n\n"
        
        if task_type == 'get_file_tree':
            result = self.mcp.get_file_tree()
            if result.get('error'):
                yield f"❌ Error: {result.get('error')}\n"
            else:
                tree_visual = format_tree_visual(result.get('tree', []))
                response = f"Here's your project structure:\n\n```\n{tree_visual}\n```"
                yield response
                self.context_history[conversation_id].append({
                    'role': 'assistant',
                    'content': response
                })
        
        elif task_type == 'read_script':
            path = params.get('path', '')
            result = self.mcp.get_script_source(path)
            
            if result.get('error'):
                yield f"❌ Error reading script: {result.get('error')}\n"
            else:
                source = result.get('content', [{}])[0].get('text', '') if isinstance(result.get('content'), list) else result.get('source', '')
                response = f"Here's the content of `{path}`:\n\n```lua\n{source}\n```"
                yield response
                self.context_history[conversation_id].append({
                    'role': 'assistant',
                    'content': response
                })
    
    def _fallback_plan(self, user_message):
        """Fallback plan when advanced planning fails"""
        return [{
            'type': 'chat',
            'description': 'Provide guidance',
            'params': {},
            'reasoning': 'Using chat mode as fallback'
        }]
    
    def _create_summary_prompt(self, user_message, context, task_plan, execution_result):
        """Create prompt for AI to generate intelligent summary"""
        
        prompt = f"""You are RoboVibeCode, an expert Roblox AI assistant. 

User asked: "{user_message}"

Execution Summary:
- Completed {execution_result.get('completed_tasks', 0)} of {execution_result.get('total_tasks', 0)} tasks
- Success rate: {(execution_result.get('completed_tasks', 0) / max(execution_result.get('total_tasks', 1), 1) * 100):.0f}%

Tasks executed:
"""
        for i, task in enumerate(task_plan, 1):
            prompt += f"{i}. {task.get('description', 'Unknown')}\n"
        
        if execution_result.get('errors'):
            prompt += "\nIssues encountered:\n"
            for error in execution_result['errors']:
                prompt += f"- {error.get('task')}: {error.get('error')}\n"
        
        prompt += """
Generate a helpful, concise response that:
1. Confirms what was accomplished
2. Explains any issues and how they were handled (if applicable)
3. Provides next steps or guidance if needed
4. Is friendly and professional

Keep it brief (2-3 sentences max). Do not repeat the user's request."""
        
        return prompt
    
    def _generate_fallback_summary(self, task_plan, execution_result):
        """Generate summary when AI fails"""
        
        summary = "Execution complete!\n\n"
        
        completed = execution_result.get('completed_tasks', 0)
        total = execution_result.get('total_tasks', 0)
        
        if completed == total and total > 0:
            summary += f"✅ Successfully completed all {total} tasks!\n\n"
        elif completed > 0:
            summary += f"⚠️ Completed {completed} of {total} tasks. Some tasks encountered issues.\n\n"
        else:
            summary += f"❌ No tasks completed successfully.\n\n"
        
        if execution_result.get('errors'):
            summary += "**Issues:**\n"
            for error in execution_result['errors'][:3]:  # Show first 3 errors
                summary += f"- {error.get('task', 'Unknown')}: {error.get('error', 'Unknown error')}\n"
        
        return summary
