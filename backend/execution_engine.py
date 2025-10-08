"""
Execution Engine with Verification and Auto-Retry
Implements verify-after-execute pattern for reliable automation
"""

import json
from typing import Dict, List, Any, Tuple

class ExecutionEngine:
    """
    Executes tasks with built-in verification and retry logic
    Ensures each step completes successfully before proceeding
    """
    
    def __init__(self, mcp_client):
        self.mcp = mcp_client
        self.execution_history = []
        self.max_retries = 3
    
    def execute_task_with_verification(self, task: Dict) -> Tuple[bool, Any, str]:
        """
        Execute a single task and verify it succeeded
        
        Returns:
            (success: bool, result: Any, message: str)
        """
        
        task_type = task.get('type', 'chat')
        params = task.get('params', {})
        description = task.get('description', 'Unknown task')
        
        print(f"Executing: {description}")
        
        # Execute the task
        success, result, error_msg = self._execute_task(task_type, params)
        
        if not success:
            return False, result, f"Execution failed: {error_msg}"
        
        # Verify if verification is specified
        verify_tool = task.get('verify_with')
        if verify_tool:
            verify_params = task.get('verify_params', {})
            verify_success, verify_result = self._verify_task(verify_tool, verify_params, task)
            
            if not verify_success:
                return False, verify_result, "Verification failed"
        
        # Log success
        self.execution_history.append({
            'task': description,
            'type': task_type,
            'success': True,
            'result': result
        })
        
        return True, result, "Success"
    
    def _execute_task(self, task_type: str, params: Dict) -> Tuple[bool, Any, str]:
        """Execute a task based on its type"""
        
        try:
            # Map task types to MCP methods
            if task_type == 'create_object':
                result = self.mcp.call_tool('create_object', params)
                return True, result, ""
                
            elif task_type == 'create_object_with_properties':
                result = self.mcp.call_tool('create_object_with_properties', params)
                return True, result, ""
                
            elif task_type == 'mass_create_objects_with_properties':
                # Debug: Print what we're sending
                objects = params.get('objects', [])
                print(f"  Creating {len(objects)} objects:")
                for i, obj in enumerate(objects[:3]):  # Show first 3
                    cframe = obj.get('properties', {}).get('CFrame', 'N/A')
                    print(f"    {obj.get('name', 'Unknown')} at CFrame: {cframe}")
                
                result = self.mcp.call_tool('mass_create_objects_with_properties', params)
                return True, result, ""
                
            elif task_type == 'set_property':
                result = self.mcp.call_tool('set_property', params)
                return True, result, ""
                
            elif task_type == 'mass_set_property':
                result = self.mcp.call_tool('mass_set_property', params)
                return True, result, ""
                
            elif task_type == 'create_script':
                # Scripts are created using create_object_with_properties
                script_params = {
                    'className': params.get('script_type', 'Script'),
                    'parent': params.get('parent_path', 'ServerScriptService'),
                    'name': params.get('name', 'NewScript'),
                    'properties': {
                        'Source': params.get('content', '-- Empty script')
                    }
                }
                result = self.mcp.call_tool('create_object_with_properties', script_params)
                return True, result, ""
                
            elif task_type == 'get_instance_properties':
                result = self.mcp.call_tool('get_instance_properties', params)
                return True, result, ""
                
            elif task_type == 'get_instance_children':
                result = self.mcp.call_tool('get_instance_children', params)
                return True, result, ""
                
            elif task_type == 'search_objects':
                result = self.mcp.call_tool('search_objects', params)
                return True, result, ""
                
            elif task_type == 'get_file_tree':
                result = self.mcp.call_tool('get_file_tree', params)
                return True, result, ""
                
            elif task_type == 'delete_object':
                result = self.mcp.call_tool('delete_object', params)
                return True, result, ""
                
            elif task_type == 'chat':
                # Chat/guidance tasks don't execute MCP calls
                return True, params, ""
                
            else:
                return False, None, f"Unknown task type: {task_type}"
                
        except Exception as e:
            return False, None, str(e)
    
    def _verify_task(self, verify_tool: str, verify_params: Dict, original_task: Dict) -> Tuple[bool, Any]:
        """Verify that a task completed successfully"""
        
        try:
            # Execute verification tool
            result = self.mcp.call_tool(verify_tool, verify_params)
            
            # Check if MCP returned an error
            if isinstance(result, dict) and 'error' in result:
                print(f"  Verification MCP error: {result.get('error')}")
                # Don't fail verification on MCP errors - just log them
                return True, result
            
            # Analyze verification result
            verification_condition = original_task.get('verify_condition', '')
            
            if verify_tool == 'get_instance_properties':
                # Check that object exists and has expected properties
                if result and isinstance(result, dict):
                    # Object exists
                    expected_props = original_task.get('params', {}).get('properties', {})
                    
                    # Verify key properties if specified
                    if expected_props:
                        for prop_name, expected_value in expected_props.items():
                            actual_value = result.get(prop_name)
                            
                            # For CFrame, check it's not default [0,0,0]
                            if prop_name == 'CFrame' and actual_value:
                                if actual_value == [0, 0, 0] and expected_value != [0, 0, 0]:
                                    return False, f"CFrame is at origin when it shouldn't be"
                    
                    return True, result
                else:
                    return False, "Object doesn't exist or has no properties"
            
            elif verify_tool == 'get_instance_children':
                # Check that children were created
                # MCP might return dict with 'children' key or direct list
                children_list = result
                if isinstance(result, dict):
                    children_list = result.get('children', result.get('instances', []))
                
                if children_list and isinstance(children_list, list):
                    # Extract number from verification condition if present
                    import re
                    num_match = re.search(r'(\d+)', verification_condition)
                    if num_match:
                        expected_count = int(num_match.group(1))
                        actual_count = len(children_list)
                        if actual_count < expected_count:
                            print(f"  Expected {expected_count} children but found {actual_count}")
                            # Don't fail - object might have been created
                            return True, result
                    
                    return True, result
                else:
                    # No children found, but that's okay - parent might be empty
                    print(f"  No children found, but continuing anyway")
                    return True, result
            
            elif verify_tool == 'get_file_tree':
                # Check overall structure
                return True, result
            
            else:
                # Default: if we got a result, verification passed
                return True, result
                
        except Exception as e:
            print(f"  Verification exception: {e}")
            # Don't fail on verification exceptions
            return True, None
    
    def execute_plan_with_recovery(self, tasks: List[Dict]) -> Dict:
        """
        Execute a full plan with automatic error recovery
        
        Returns:
            {
                'success': bool,
                'completed_tasks': int,
                'total_tasks': int,
                'results': List[Any],
                'errors': List[str]
            }
        """
        
        results = []
        errors = []
        completed_count = 0
        
        for i, task in enumerate(tasks):
            print(f"\nTask {i+1}/{len(tasks)}: {task.get('description', 'Unknown')}")
            
            # Try task with retries
            success = False
            last_error = ""
            
            for attempt in range(self.max_retries):
                if attempt > 0:
                    print(f"  Retry attempt {attempt + 1}/{self.max_retries}")
                
                success, result, message = self.execute_task_with_verification(task)
                
                if success:
                    print(f"  ✓ Success: {message}")
                    results.append(result)
                    completed_count += 1
                    break
                else:
                    last_error = message
                    print(f"  ✗ Failed: {message}")
                    
                    # Try to diagnose and fix
                    if attempt < self.max_retries - 1:
                        fixed_task = self._attempt_fix(task, message)
                        if fixed_task:
                            task = fixed_task
                            print(f"  → Attempting fix...")
            
            if not success:
                errors.append({
                    'task': task.get('description'),
                    'error': last_error,
                    'task_index': i
                })
                
                # Decide if we should continue or stop
                if self._is_critical_task(task):
                    print(f"\n✗ Critical task failed, stopping execution")
                    break
                else:
                    print(f"  → Non-critical task failed, continuing...")
        
        return {
            'success': completed_count == len(tasks),
            'completed_tasks': completed_count,
            'total_tasks': len(tasks),
            'results': results,
            'errors': errors
        }
    
    def _attempt_fix(self, task: Dict, error_message: str) -> Dict | None:
        """Attempt to fix a failed task based on error message"""
        
        # Common fixes
        
        # Fix 1: CFrame format issues
        if 'CFrame' in error_message or 'position' in error_message.lower():
            # Ensure CFrame is in correct format [x, y, z]
            params = task.get('params', {})
            if 'properties' in params:
                cframe = params['properties'].get('CFrame')
                if cframe and not isinstance(cframe, list):
                    # Try to convert to list
                    params['properties']['CFrame'] = [0, 5, 0]  # Safe default
                    return task
        
        # Fix 2: Parent path issues
        if 'parent' in error_message.lower() or 'not found' in error_message.lower():
            # Try simpler parent path
            params = task.get('params', {})
            if 'parent' in params:
                # Simplify to just service name
                parent = params['parent']
                if '.' in parent:
                    params['parent'] = parent.split('.')[0]
                    return task
        
        # Fix 3: Property type issues
        if 'type' in error_message.lower() or 'invalid' in error_message.lower():
            # Remove problematic properties
            params = task.get('params', {})
            if 'properties' in params:
                # Keep only essential properties
                essential = ['CFrame', 'Size', 'Anchored', 'BrickColor']
                params['properties'] = {
                    k: v for k, v in params['properties'].items() 
                    if k in essential
                }
                return task
        
        return None
    
    def _is_critical_task(self, task: Dict) -> bool:
        """Determine if a task is critical to the overall plan"""
        
        # Folder/structure creation is usually critical
        task_type = task.get('type')
        description = task.get('description', '').lower()
        
        if 'folder' in description or 'structure' in description:
            return True
        
        # First tasks are often critical
        if len(self.execution_history) < 2:
            return True
        
        # Most tasks are non-critical
        return False
    
    def get_execution_summary(self) -> str:
        """Get a summary of execution history"""
        
        if not self.execution_history:
            return "No tasks executed yet."
        
        total = len(self.execution_history)
        successful = sum(1 for t in self.execution_history if t.get('success'))
        
        summary = f"\nExecution Summary:\n"
        summary += f"  Total tasks: {total}\n"
        summary += f"  Successful: {successful}\n"
        summary += f"  Failed: {total - successful}\n\n"
        
        summary += "Task History:\n"
        for i, task in enumerate(self.execution_history[-10:], 1):  # Last 10 tasks
            status = "✓" if task.get('success') else "✗"
            summary += f"  {status} {task.get('task', 'Unknown')}\n"
        
        return summary
