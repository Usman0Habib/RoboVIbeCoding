"""
Spatial Reasoning Engine - Handles 3D positioning, CFrame calculations, and layout planning
Solves the critical problem of objects spawning at the same location
"""

import math
from typing import List, Dict, Tuple, Any

class SpatialEngine:
    """Calculates proper 3D positions and CFrame values for Roblox objects"""
    
    @staticmethod
    def vector3_to_cframe(x, y, z):
        """Convert Vector3 position to CFrame format for Roblox (Rojo v7 format)"""
        return {
            "position": [float(x), float(y), float(z)],
            "orientation": [
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0]
            ]
        }
    
    @staticmethod
    def calculate_obby_platforms(num_platforms, difficulty='medium'):
        """
        Calculate positions for obby platforms with proper spacing
        
        Args:
            num_platforms: Number of platforms to create
            difficulty: 'easy', 'medium', 'hard' - affects jump distance and height variation
        
        Returns:
            List of platform configurations with CFrame positions
        """
        platforms = []
        
        # Difficulty settings
        settings = {
            'easy': {'x_spacing': 8, 'z_spacing': 0, 'y_variation': 2, 'platform_size': [8, 1, 8]},
            'medium': {'x_spacing': 10, 'z_spacing': 2, 'y_variation': 3, 'platform_size': [6, 1, 6]},
            'hard': {'x_spacing': 12, 'z_spacing': 4, 'y_variation': 4, 'platform_size': [4, 1, 4]}
        }
        
        config = settings.get(difficulty, settings['medium'])
        
        # Starting position
        current_x = 0
        current_y = 5
        current_z = 0
        
        for i in range(num_platforms):
            # Calculate position with variation
            if i > 0:
                current_x += config['x_spacing']
                current_z += (-1 if i % 2 == 0 else 1) * config['z_spacing']
                
                # Add height variation
                if i % 3 == 0:
                    current_y += config['y_variation']
                elif i % 3 == 1:
                    current_y -= config['y_variation'] // 2
            
            platforms.append({
                'name': f'Platform{i + 1}',
                'className': 'Part',
                'parent': 'game.Workspace',
                'properties': {
                    'CFrame': SpatialEngine.vector3_to_cframe(current_x, current_y, current_z),
                    'Size': config['platform_size'],
                    'BrickColor': SpatialEngine.get_obby_color(i),
                    'Material': 'Plastic',
                    'Anchored': True
                }
            })
        
        return platforms
    
    @staticmethod
    def get_obby_color(index):
        """Get color for obby platform based on index"""
        colors = [
            'Bright blue', 'Bright green', 'Bright yellow', 
            'Bright orange', 'Bright red', 'Bright violet'
        ]
        return colors[index % len(colors)]
    
    @staticmethod
    def calculate_grid_layout(num_objects, object_size, spacing=2):
        """
        Calculate grid layout positions for multiple objects
        
        Args:
            num_objects: Number of objects to position
            object_size: [x, y, z] size of each object
            spacing: Gap between objects
        
        Returns:
            List of CFrame positions
        """
        positions = []
        grid_size = math.ceil(math.sqrt(num_objects))
        
        x_step = object_size[0] + spacing
        z_step = object_size[2] + spacing
        
        for i in range(num_objects):
            row = i // grid_size
            col = i % grid_size
            
            x = col * x_step
            y = object_size[1] / 2
            z = row * z_step
            
            positions.append(SpatialEngine.vector3_to_cframe(x, y, z))
        
        return positions
    
    @staticmethod
    def calculate_circular_layout(num_objects, radius=20, height=5):
        """
        Calculate circular layout positions (useful for arenas, spawn points)
        
        Args:
            num_objects: Number of objects to arrange in circle
            radius: Radius of circle
            height: Y position of objects
        
        Returns:
            List of CFrame positions
        """
        positions = []
        angle_step = (2 * math.pi) / num_objects
        
        for i in range(num_objects):
            angle = i * angle_step
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            
            positions.append(SpatialEngine.vector3_to_cframe(x, height, z))
        
        return positions
    
    @staticmethod
    def calculate_staircase(num_steps, step_size=[10, 1, 4], rise=1, run=4):
        """
        Calculate positions for a staircase
        
        Args:
            num_steps: Number of steps
            step_size: [x, y, z] size of each step
            rise: Height increase per step
            run: Forward distance per step
        
        Returns:
            List of step configurations
        """
        steps = []
        
        for i in range(num_steps):
            steps.append({
                'name': f'Step{i + 1}',
                'className': 'Part',
                'parent': 'game.Workspace',
                'properties': {
                    'CFrame': SpatialEngine.vector3_to_cframe(
                        0,
                        i * rise + step_size[1] / 2,
                        i * run
                    ),
                    'Size': step_size,
                    'BrickColor': 'Dark stone grey',
                    'Material': 'Slate',
                    'Anchored': True
                }
            })
        
        return steps
    
    @staticmethod
    def calculate_building_layout(building_type, size='medium'):
        """
        Calculate layout for common building types
        
        Args:
            building_type: 'house', 'tower', 'shop', etc.
            size: 'small', 'medium', 'large'
        
        Returns:
            List of object configurations for the building
        """
        if building_type == 'house':
            return SpatialEngine._create_house(size)
        elif building_type == 'tower':
            return SpatialEngine._create_tower(size)
        elif building_type == 'shop':
            return SpatialEngine._create_shop(size)
        else:
            return []
    
    @staticmethod
    def _create_house(size):
        """Create a simple house structure"""
        sizes = {
            'small': {'base': [20, 10, 15], 'roof_height': 8},
            'medium': {'base': [30, 12, 25], 'roof_height': 10},
            'large': {'base': [40, 15, 35], 'roof_height': 12}
        }
        config = sizes.get(size, sizes['medium'])
        
        base_size = config['base']
        objects = []
        
        # Floor
        objects.append({
            'name': 'HouseFloor',
            'className': 'Part',
            'parent': 'Workspace',
            'properties': {
                'CFrame': SpatialEngine.vector3_to_cframe(0, 0.5, 0),
                'Size': [base_size[0], 1, base_size[2]],
                'BrickColor': 'Dark stone grey',
                'Material': 'Concrete',
                'Anchored': True
            }
        })
        
        # Walls (4 sides)
        wall_thickness = 1
        wall_height = base_size[1]
        
        # Front wall
        objects.append({
            'name': 'HouseFrontWall',
            'className': 'Part',
            'parent': 'Workspace',
            'properties': {
                'CFrame': SpatialEngine.vector3_to_cframe(0, wall_height/2, -base_size[2]/2),
                'Size': [base_size[0], wall_height, wall_thickness],
                'BrickColor': 'Brick yellow',
                'Material': 'Brick',
                'Anchored': True
            }
        })
        
        # Back wall
        objects.append({
            'name': 'HouseBackWall',
            'className': 'Part',
            'parent': 'Workspace',
            'properties': {
                'CFrame': SpatialEngine.vector3_to_cframe(0, wall_height/2, base_size[2]/2),
                'Size': [base_size[0], wall_height, wall_thickness],
                'BrickColor': 'Brick yellow',
                'Material': 'Brick',
                'Anchored': True
            }
        })
        
        # Left wall
        objects.append({
            'name': 'HouseLeftWall',
            'className': 'Part',
            'parent': 'Workspace',
            'properties': {
                'CFrame': SpatialEngine.vector3_to_cframe(-base_size[0]/2, wall_height/2, 0),
                'Size': [wall_thickness, wall_height, base_size[2]],
                'BrickColor': 'Brick yellow',
                'Material': 'Brick',
                'Anchored': True
            }
        })
        
        # Right wall
        objects.append({
            'name': 'HouseRightWall',
            'className': 'Part',
            'parent': 'Workspace',
            'properties': {
                'CFrame': SpatialEngine.vector3_to_cframe(base_size[0]/2, wall_height/2, 0),
                'Size': [wall_thickness, wall_height, base_size[2]],
                'BrickColor': 'Brick yellow',
                'Material': 'Brick',
                'Anchored': True
            }
        })
        
        # Roof
        objects.append({
            'name': 'HouseRoof',
            'className': 'WedgePart',
            'parent': 'Workspace',
            'properties': {
                'CFrame': SpatialEngine.vector3_to_cframe(0, wall_height + config['roof_height']/2, 0),
                'Size': [base_size[0], config['roof_height'], base_size[2]],
                'BrickColor': 'Dark orange',
                'Material': 'Slate',
                'Anchored': True
            }
        })
        
        return objects
    
    @staticmethod
    def _create_tower(size):
        """Create a simple tower structure"""
        sizes = {
            'small': {'base': 8, 'floors': 5, 'floor_height': 4},
            'medium': {'base': 12, 'floors': 8, 'floor_height': 5},
            'large': {'base': 16, 'floors': 12, 'floor_height': 6}
        }
        config = sizes.get(size, sizes['medium'])
        
        objects = []
        
        for floor in range(config['floors']):
            y_pos = floor * config['floor_height'] + 0.5
            
            objects.append({
                'name': f'TowerFloor{floor + 1}',
                'className': 'Part',
                'parent': 'game.Workspace',
                'properties': {
                    'CFrame': SpatialEngine.vector3_to_cframe(0, y_pos, 0),
                    'Size': [config['base'], 1, config['base']],
                    'BrickColor': 'Medium stone grey' if floor % 2 == 0 else 'Dark stone grey',
                    'Material': 'Concrete',
                    'Anchored': True
                }
            })
        
        return objects
    
    @staticmethod
    def _create_shop(size):
        """Create a simple shop structure"""
        # Similar to house but with different dimensions and colors
        return SpatialEngine._create_house(size)
    
    @staticmethod
    def calculate_path_points(start_pos, end_pos, num_points, curve_amount=0):
        """
        Calculate points along a path from start to end
        
        Args:
            start_pos: [x, y, z] starting position
            end_pos: [x, y, z] ending position
            num_points: Number of points along path
            curve_amount: 0 = straight line, >0 = curved path
        
        Returns:
            List of CFrame positions along the path
        """
        positions = []
        
        for i in range(num_points):
            t = i / (num_points - 1) if num_points > 1 else 0
            
            x = start_pos[0] + (end_pos[0] - start_pos[0]) * t
            y = start_pos[1] + (end_pos[1] - start_pos[1]) * t
            z = start_pos[2] + (end_pos[2] - start_pos[2]) * t
            
            # Add curve if specified
            if curve_amount > 0:
                # Parabolic curve
                curve_offset = curve_amount * math.sin(t * math.pi)
                y += curve_offset
            
            positions.append(SpatialEngine.vector3_to_cframe(x, y, z))
        
        return positions
    
    @staticmethod
    def get_spawn_location(platform_cframe, platform_size):
        """
        Calculate spawn location above a platform
        
        Args:
            platform_cframe: CFrame dict with position/orientation (Rojo v7 format)
            platform_size: [x, y, z] size of platform
        
        Returns:
            CFrame for SpawnLocation
        """
        # Extract position from Rojo v7 format
        if isinstance(platform_cframe, dict) and 'position' in platform_cframe:
            pos = platform_cframe['position']
            x, y, z = pos[0], pos[1], pos[2]
        else:
            # Fallback for old format
            x, y, z = platform_cframe[0], platform_cframe[1], platform_cframe[2]
        
        return SpatialEngine.vector3_to_cframe(
            x,
            y + platform_size[1]/2 + 2.5,  # 2.5 studs above platform
            z
        )
