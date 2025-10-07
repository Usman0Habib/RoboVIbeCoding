def get_object_creation_script(object_type, name, properties=None):
    """Generate Lua script to create Roblox objects"""
    properties = properties or {}
    
    if object_type.lower() in ['cube', 'part', 'block']:
        return generate_part_script(name, properties)
    elif object_type.lower() in ['sphere', 'ball']:
        return generate_sphere_script(name, properties)
    elif object_type.lower() == 'cylinder':
        return generate_cylinder_script(name, properties)
    elif object_type.lower() == 'folder':
        return generate_folder_script(name, properties)
    elif object_type.lower() == 'model':
        return generate_model_script(name, properties)
    else:
        return generate_generic_instance_script(object_type, name, properties)

def generate_part_script(name, properties):
    """Generate script to create a Part (cube)"""
    size = properties.get('size', [4, 4, 4])
    position = properties.get('position', [0, 10, 0])
    color = properties.get('color', None)
    material = properties.get('material', 'Plastic')
    parent = properties.get('parent', 'Workspace')
    anchored = properties.get('anchored', True)
    
    size_str = f"Vector3.new({size[0]}, {size[1]}, {size[2]})"
    pos_str = f"Vector3.new({position[0]}, {position[1]}, {position[2]})"
    
    color_line = ""
    if color:
        if isinstance(color, list) and len(color) == 3:
            color_line = f"part.Color = Color3.new({color[0]}, {color[1]}, {color[2]})"
        elif isinstance(color, str):
            color_line = f"part.BrickColor = BrickColor.new('{color}')"
    
    script = f"""-- Auto-generated script to create {name}
local part = Instance.new("Part")
part.Name = "{name}"
part.Size = {size_str}
part.Position = {pos_str}
part.Material = Enum.Material.{material}
part.Anchored = {str(anchored).lower()}
{color_line}
part.Parent = game.{parent}

print("✅ Created part: {name}")
"""
    return script.strip()

def generate_sphere_script(name, properties):
    """Generate script to create a Sphere"""
    size = properties.get('size', [4, 4, 4])
    position = properties.get('position', [0, 10, 0])
    color = properties.get('color', None)
    material = properties.get('material', 'Plastic')
    parent = properties.get('parent', 'Workspace')
    anchored = properties.get('anchored', True)
    
    size_str = f"Vector3.new({size[0]}, {size[1]}, {size[2]})"
    pos_str = f"Vector3.new({position[0]}, {position[1]}, {position[2]})"
    
    color_line = ""
    if color:
        if isinstance(color, list) and len(color) == 3:
            color_line = f"part.Color = Color3.new({color[0]}, {color[1]}, {color[2]})"
        elif isinstance(color, str):
            color_line = f"part.BrickColor = BrickColor.new('{color}')"
    
    script = f"""-- Auto-generated script to create {name}
local part = Instance.new("Part")
part.Name = "{name}"
part.Size = {size_str}
part.Position = {pos_str}
part.Shape = Enum.PartType.Ball
part.Material = Enum.Material.{material}
part.Anchored = {str(anchored).lower()}
{color_line}
part.Parent = game.{parent}

print("✅ Created sphere: {name}")
"""
    return script.strip()

def generate_cylinder_script(name, properties):
    """Generate script to create a Cylinder"""
    size = properties.get('size', [4, 4, 4])
    position = properties.get('position', [0, 10, 0])
    color = properties.get('color', None)
    material = properties.get('material', 'Plastic')
    parent = properties.get('parent', 'Workspace')
    anchored = properties.get('anchored', True)
    
    size_str = f"Vector3.new({size[0]}, {size[1]}, {size[2]})"
    pos_str = f"Vector3.new({position[0]}, {position[1]}, {position[2]})"
    
    color_line = ""
    if color:
        if isinstance(color, list) and len(color) == 3:
            color_line = f"part.Color = Color3.new({color[0]}, {color[1]}, {color[2]})"
        elif isinstance(color, str):
            color_line = f"part.BrickColor = BrickColor.new('{color}')"
    
    script = f"""-- Auto-generated script to create {name}
local part = Instance.new("Part")
part.Name = "{name}"
part.Size = {size_str}
part.Position = {pos_str}
part.Shape = Enum.PartType.Cylinder
part.Material = Enum.Material.{material}
part.Anchored = {str(anchored).lower()}
{color_line}
part.Parent = game.{parent}

print("✅ Created cylinder: {name}")
"""
    return script.strip()

def generate_folder_script(name, properties):
    """Generate script to create a Folder"""
    parent = properties.get('parent', 'Workspace')
    
    script = f"""-- Auto-generated script to create {name}
local folder = Instance.new("Folder")
folder.Name = "{name}"
folder.Parent = game.{parent}

print("✅ Created folder: {name}")
"""
    return script.strip()

def generate_model_script(name, properties):
    """Generate script to create a Model"""
    parent = properties.get('parent', 'Workspace')
    primary_part = properties.get('primary_part', None)
    
    primary_line = ""
    if primary_part:
        primary_line = f'model.PrimaryPart = model:FindFirstChild("{primary_part}")'
    
    script = f"""-- Auto-generated script to create {name}
local model = Instance.new("Model")
model.Name = "{name}"
{primary_line}
model.Parent = game.{parent}

print("✅ Created model: {name}")
"""
    return script.strip()

def generate_generic_instance_script(object_type, name, properties):
    """Generate script to create any Roblox Instance"""
    parent = properties.get('parent', 'Workspace')
    
    properties_lines = []
    for key, value in properties.items():
        if key not in ['parent']:
            if isinstance(value, str):
                properties_lines.append(f'instance.{key} = "{value}"')
            elif isinstance(value, bool):
                properties_lines.append(f'instance.{key} = {str(value).lower()}')
            else:
                properties_lines.append(f'instance.{key} = {value}')
    
    properties_str = '\n'.join(properties_lines)
    
    script = f"""-- Auto-generated script to create {name}
local instance = Instance.new("{object_type}")
instance.Name = "{name}"
{properties_str}
instance.Parent = game.{parent}

print("✅ Created {object_type}: {name}")
"""
    return script.strip()

def parse_object_command(message):
    """Parse user message to extract object creation parameters"""
    message_lower = message.lower()
    
    result = {
        'type': 'part',
        'name': 'Object',
        'properties': {}
    }
    
    if 'cube' in message_lower or 'block' in message_lower:
        result['type'] = 'cube'
        result['name'] = 'Cube'
    elif 'sphere' in message_lower or 'ball' in message_lower:
        result['type'] = 'sphere'
        result['name'] = 'Sphere'
    elif 'cylinder' in message_lower:
        result['type'] = 'cylinder'
        result['name'] = 'Cylinder'
    elif 'folder' in message_lower:
        result['type'] = 'folder'
        result['name'] = 'Folder'
    elif 'model' in message_lower:
        result['type'] = 'model'
        result['name'] = 'Model'
    
    import re
    
    size_match = re.search(r'size\s+(\d+)\s*[,x]?\s*(\d+)\s*[,x]?\s*(\d+)', message_lower)
    if size_match:
        result['properties']['size'] = [int(size_match.group(1)), int(size_match.group(2)), int(size_match.group(3))]
    
    pos_match = re.search(r'(?:position|pos|at)\s+(-?\d+)\s*[,]?\s*(-?\d+)\s*[,]?\s*(-?\d+)', message_lower)
    if pos_match:
        result['properties']['position'] = [int(pos_match.group(1)), int(pos_match.group(2)), int(pos_match.group(3))]
    
    color_match = re.search(r'color\s+([a-z]+)', message_lower)
    if color_match:
        result['properties']['color'] = color_match.group(1).capitalize()
    
    if 'red' in message_lower and 'color' not in result['properties']:
        result['properties']['color'] = 'Bright red'
    elif 'blue' in message_lower and 'color' not in result['properties']:
        result['properties']['color'] = 'Bright blue'
    elif 'green' in message_lower and 'color' not in result['properties']:
        result['properties']['color'] = 'Bright green'
    
    name_match = re.search(r'(?:named|called)\s+["\']?([^"\']+)["\']?', message)
    if name_match:
        result['name'] = name_match.group(1).strip()
    
    return result
