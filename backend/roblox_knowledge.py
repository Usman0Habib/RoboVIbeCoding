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
}

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
