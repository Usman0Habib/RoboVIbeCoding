ROBLOX_SYSTEM_PROMPT = """You are RoboVibeCode, an expert autonomous AI agent specialized in Roblox Studio development and Lua scripting.

CORE CAPABILITIES:
- You can create, read, modify, and organize Roblox scripts and objects
- You understand Roblox Studio architecture, services, and best practices
- You write production-quality Lua code following Roblox standards
- You can build complete game systems autonomously

ROBLOX KNOWLEDGE:
1. Services (always access via game:GetService()):
   - ReplicatedStorage: Shared containers for RemoteEvents, RemoteFunctions, and shared modules
   - ServerScriptService: Server-side scripts (high security)
   - StarterPlayer.StarterPlayerScripts: Client-side LocalScripts
   - StarterGui: UI elements that clone to each player
   - Workspace: Physical game world objects
   - Players: Player management
   - DataStoreService: Persistent data storage
   - HttpService: External web requests
   - TweenService: Smooth animations
   - UserInputService: Input handling

2. Script Types:
   - Script: Server-side execution
   - LocalScript: Client-side execution (in StarterGui, StarterPlayerScripts, or player's character)
   - ModuleScript: Reusable code modules (require() to use)

3. Remote Communication (Client-Server):
   - RemoteEvent: One-way communication (FireServer, FireClient, FireAllClients)
   - RemoteFunction: Two-way communication with return values (InvokeServer, InvokeClient)
   - Always validate on server, never trust client

4. Best Practices:
   - Use WaitForChild() for objects that may not exist immediately
   - Avoid wait() in loops, use task.wait() or Heartbeat
   - Implement proper error handling with pcall()
   - Use CollectionService for tags and grouped object management
   - Optimize with object pooling for frequently created/destroyed objects
   - Keep client and server logic separated

5. Common Patterns:
   - Leaderstats: IntValue/StringValue in player.leaderstats folder
   - Data persistence: DataStoreService with UpdateAsync
   - GUI updates: RemoteEvent to update client UI
   - Character loading: player.CharacterAdded event

TASK EXECUTION:
When given a request:
1. Analyze what needs to be created/modified
2. Break down into logical steps
3. Generate complete, working Lua code
4. Organize code properly in Roblox hierarchy
5. Include error handling and validation
6. Follow Roblox security best practices

CODE STYLE:
- Use PascalCase for functions and variables
- Clear, descriptive names
- Comment complex logic
- Proper indentation
- Modular, reusable code

Always provide complete, working solutions that can be directly implemented in Roblox Studio."""

ROBLOX_CODE_TEMPLATES = {
    'remote_event_server': '''local ReplicatedStorage = game:GetService("ReplicatedStorage")
local {event_name} = ReplicatedStorage:WaitForChild("{event_name}")

{event_name}.OnServerEvent:Connect(function(player, ...)
    -- Server-side handling
    print(player.Name .. " triggered event")
end)''',
    
    'remote_event_client': '''local ReplicatedStorage = game:GetService("ReplicatedStorage")
local {event_name} = ReplicatedStorage:WaitForChild("{event_name}")

{event_name}:FireServer(data)''',
    
    'datastore_save': '''local DataStoreService = game:GetService("DataStoreService")
local {store_name} = DataStoreService:GetDataStore("{store_name}")

local function SaveData(player)
    local success, result = pcall(function()
        local data = {
            -- Add player data here
        }
        {store_name}:SetAsync(player.UserId, data)
    end)
    
    if not success then
        warn("Failed to save data for " .. player.Name .. ": " .. tostring(result))
    end
end

game.Players.PlayerRemoving:Connect(SaveData)''',
    
    'leaderstats': '''game.Players.PlayerAdded:Connect(function(player)
    local leaderstats = Instance.new("Folder")
    leaderstats.Name = "leaderstats"
    leaderstats.Parent = player
    
    local {stat_name} = Instance.new("IntValue")
    {stat_name}.Name = "{stat_display_name}"
    {stat_name}.Value = 0
    {stat_name}.Parent = leaderstats
end)''',
    
    'module_script': '''local {module_name} = {}

function {module_name}.{function_name}(...)
    -- Implementation
end

return {module_name}''',
    
    'checkpoint_system': '''-- Checkpoint System for Obby Games
local Players = game:GetService("Players")
local checkpoints = workspace:WaitForChild("Checkpoints"):GetChildren()

-- Sort checkpoints by name
table.sort(checkpoints, function(a, b)
    return tonumber(a.Name:match("%d+")) < tonumber(b.Name:match("%d+"))
end)

local playerCheckpoints = {}

Players.PlayerAdded:Connect(function(player)
    playerCheckpoints[player.UserId] = 1
    
    player.CharacterAdded:Connect(function(character)
        local humanoid = character:WaitForChild("Humanoid")
        local hrp = character:WaitForChild("HumanoidRootPart")
        
        -- Teleport to last checkpoint
        local checkpointIndex = playerCheckpoints[player.UserId] or 1
        if checkpoints[checkpointIndex] then
            hrp.CFrame = checkpoints[checkpointIndex].CFrame + Vector3.new(0, 3, 0)
        end
        
        -- Death handling
        humanoid.Died:Connect(function()
            task.wait(2)
            player:LoadCharacter()
        end)
    end)
end)

-- Checkpoint touch detection
for i, checkpoint in ipairs(checkpoints) do
    checkpoint.Touched:Connect(function(hit)
        local character = hit.Parent
        local player = Players:GetPlayerFromCharacter(character)
        
        if player and playerCheckpoints[player.UserId] == i then
            playerCheckpoints[player.UserId] = i + 1
            checkpoint.BrickColor = BrickColor.new("Bright green")
            checkpoint.Material = Enum.Material.Neon
        end
    end)
end''',
    
    'tween_service_movement': '''local TweenService = game:GetService("TweenService")

local function MovePart(part, targetCFrame, duration)
    local tweenInfo = TweenInfo.new(
        duration,
        Enum.EasingStyle.Quad,
        Enum.EasingDirection.InOut
    )
    
    local tween = TweenService:Create(part, tweenInfo, {CFrame = targetCFrame})
    tween:Play()
    
    return tween
end

-- Example usage:
-- MovePart(workspace.MovingPlatform, CFrame.new(0, 10, 0), 2)''',
    
    'kill_brick': '''-- Kill brick that respawns player
local killBrick = script.Parent

killBrick.Touched:Connect(function(hit)
    local humanoid = hit.Parent:FindFirstChild("Humanoid")
    if humanoid then
        humanoid.Health = 0
    end
end)''',
}

# Property templates for common objects with correct types
ROBLOX_PROPERTY_TEMPLATES = {
    'Part': {
        'default': {
            'Anchored': True,
            'Size': [4, 1, 4],
            'BrickColor': 'Medium stone grey',
            'Material': 'Plastic'
        },
        'platform': {
            'Anchored': True,
            'Size': [10, 1, 10],
            'BrickColor': 'Bright blue',
            'Material': 'Plastic',
            'TopSurface': 'Smooth',
            'BottomSurface': 'Smooth'
        },
        'wall': {
            'Anchored': True,
            'Size': [1, 10, 20],
            'BrickColor': 'Brick yellow',
            'Material': 'Brick'
        },
        'kill_brick': {
            'Anchored': True,
            'Size': [10, 1, 10],
            'BrickColor': 'Really red',
            'Material': 'Neon',
            'Transparency': 0.3
        }
    },
    'SpawnLocation': {
        'default': {
            'Anchored': True,
            'Size': [6, 1, 6],
            'BrickColor': 'Bright green',
            'Material': 'Plastic',
            'Transparency': 0,
            'Duration': 0,
            'Neutral': False
        }
    },
    'Script': {
        'default': {
            'Source': '-- Script content here'
        }
    },
    'LocalScript': {
        'default': {
            'Source': '-- LocalScript content here'
        }
    },
    'ModuleScript': {
        'default': {
            'Source': 'local module = {}\n\nreturn module'
        }
    }
}

def get_property_template(object_type, template_name='default'):
    """Get property template for an object type"""
    if object_type in ROBLOX_PROPERTY_TEMPLATES:
        templates = ROBLOX_PROPERTY_TEMPLATES[object_type]
        return templates.get(template_name, templates.get('default', {}))
    return {}

def get_roblox_context():
    return ROBLOX_SYSTEM_PROMPT

def get_template(template_name, **kwargs):
    if template_name in ROBLOX_CODE_TEMPLATES:
        return ROBLOX_CODE_TEMPLATES[template_name].format(**kwargs)
    return None

def generate_roblox_structure_suggestion(game_type):
    structures = {
        'obby': {
            'description': 'Obstacle course game with checkpoints and levels',
            'folders': [
                'ReplicatedStorage/Checkpoints',
                'ReplicatedStorage/RemoteEvents',
                'ServerScriptService/CheckpointManager',
                'StarterGui/ObbyUI',
            ],
            'scripts': [
                ('ServerScriptService/CheckpointManager', 'Script'),
                ('StarterPlayer/StarterPlayerScripts/ClientController', 'LocalScript'),
            ]
        },
        'tycoon': {
            'description': 'Tycoon game with money, buttons, and upgrades',
            'folders': [
                'ReplicatedStorage/TycoonData',
                'ServerScriptService/TycoonManager',
                'ServerScriptService/DataManager',
            ],
            'scripts': [
                ('ServerScriptService/TycoonManager/MainController', 'Script'),
                ('ServerScriptService/DataManager/SaveSystem', 'Script'),
            ]
        },
        'rpg': {
            'description': 'RPG with inventory, quests, and combat',
            'folders': [
                'ReplicatedStorage/GameData',
                'ReplicatedStorage/RemoteEvents',
                'ServerScriptService/CombatSystem',
                'ServerScriptService/InventorySystem',
                'ServerScriptService/QuestSystem',
            ],
            'scripts': [
                ('ReplicatedStorage/GameData/ItemDatabase', 'ModuleScript'),
                ('ServerScriptService/CombatSystem/DamageHandler', 'Script'),
            ]
        }
    }
    
    return structures.get(game_type.lower(), None)
