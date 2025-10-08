#!/usr/bin/env python3
import requests
import json
import time

def send_prompt_to_robovibe(message, conversation_id="obby_build"):
    """Send a well-crafted prompt to RoboVibeCode"""
    url = "http://localhost:5000/api/stream-chat"
    
    payload = {
        "message": message,
        "conversation_id": conversation_id
    }
    
    print(f"\n{'='*80}")
    print(f"📤 SENDING PROMPT:")
    print(f"{'='*80}")
    print(message)
    print(f"{'='*80}\n")
    
    try:
        response = requests.post(url, json=payload, stream=True, timeout=120)
        
        print("📥 RESPONSE:")
        print("-" * 80)
        
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data = json.loads(line[6:])
                    if 'chunk' in data:
                        print(data['chunk'], end='', flush=True)
                    elif 'done' in data:
                        print("\n" + "-" * 80)
                        print("✅ Completed!")
                        break
                    elif 'error' in data:
                        print(f"\n❌ Error: {data['error']}")
                        break
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🤖 RoboVibeCode AI Prompt Optimizer")
    print("="*80)
    print("Crafting expert prompts for Gemini to build a professional obby...")
    print("="*80)
    
    # Step 1: Clean workspace with specific instructions
    prompt1 = """TASK: Clean Workspace

Before building the obby, I need you to:

1. Get the current project structure using get_file_tree
2. Identify and DELETE all test objects in Workspace that match these patterns:
   - Any parts named with "Test", "Demo", "Example"
   - Scripts in ServerScriptService that look like tests
   - Any folders named "Testing" or similar
3. Confirm what was deleted

Be thorough and list what you're deleting."""

    # Step 2: Build foundation with exact specifications
    prompt2 = """TASK: Create Obby Foundation Structure

Create the following EXACT structure in Workspace:

1. CREATE FOLDER: "HighDifficultyObby" in Workspace

2. CREATE SPAWN AREA:
   - Part Name: "SpawnPlatform"
   - Parent: Workspace.HighDifficultyObby
   - Position: Vector3.new(0, 5, 0)
   - Size: Vector3.new(12, 1, 12)
   - BrickColor: "Bright green"
   - Material: "Plastic"
   - Anchored: true

3. CREATE CHECKPOINT FOLDER:
   - Folder Name: "Checkpoints"
   - Parent: Workspace.HighDifficultyObby

4. CREATE FINISH AREA (at end):
   - Part Name: "FinishPlatform"
   - Parent: Workspace.HighDifficultyObby
   - Position: Vector3.new(0, 50, 200)
   - Size: Vector3.new(15, 1, 15)
   - BrickColor: "Gold"
   - Material: "Neon"
   - Anchored: true

Confirm each creation with its exact properties."""

    # Step 3: Level 1-3 (Easy) with precise specs
    prompt3 = """TASK: Build Levels 1-3 (EASY WARMUP)

Create these platforms with EXACT specifications:

LEVEL 1 - Basic Jumps:
1. Part: "Level1_P1" | Parent: Workspace.HighDifficultyObby | Pos: (0, 5, 15) | Size: (8, 1, 8) | Color: "Bright blue"
2. Part: "Level1_P2" | Parent: Workspace.HighDifficultyObby | Pos: (0, 7, 25) | Size: (6, 1, 6) | Color: "Bright blue"
3. Part: "Level1_P3" | Parent: Workspace.HighDifficultyObby | Pos: (0, 9, 35) | Size: (5, 1, 5) | Color: "Bright blue"

LEVEL 2 - Narrow Platforms:
1. Part: "Level2_P1" | Parent: Workspace.HighDifficultyObby | Pos: (5, 11, 40) | Size: (4, 1, 4) | Color: "Bright yellow"
2. Part: "Level2_P2" | Parent: Workspace.HighDifficultyObby | Pos: (-5, 13, 45) | Size: (3, 1, 3) | Color: "Bright yellow"
3. Part: "Level2_P3" | Parent: Workspace.HighDifficultyObby | Pos: (0, 15, 50) | Size: (3, 1, 3) | Color: "Bright yellow"

LEVEL 3 - Diagonal Jumps:
1. Part: "Level3_P1" | Parent: Workspace.HighDifficultyObby | Pos: (7, 17, 55) | Size: (2.5, 1, 2.5) | Color: "Bright orange"
2. Part: "Level3_P2" | Parent: Workspace.HighDifficultyObby | Pos: (-7, 19, 60) | Size: (2, 1, 2) | Color: "Bright orange"
3. Part: "Level3_P3" | Parent: Workspace.HighDifficultyObby | Pos: (0, 21, 65) | Size: (2, 1, 2) | Color: "Bright orange"

All parts MUST have Anchored = true. Use create_object_with_properties for each."""

    # Step 4: Levels 4-7 (Medium) with moving parts
    prompt4 = """TASK: Build Levels 4-7 (MEDIUM DIFFICULTY)

Create these challenging platforms:

LEVEL 4 - Precision Jumps:
1. Part: "Level4_P1" | Pos: (8, 23, 70) | Size: (2, 1, 2) | Color: "Bright red"
2. Part: "Level4_P2" | Pos: (-8, 25, 75) | Size: (1.5, 1, 1.5) | Color: "Bright red"
3. Part: "Level4_P3" | Pos: (0, 27, 80) | Size: (1.5, 1, 1.5) | Color: "Bright red"

LEVEL 5 - Scattered Platforms:
1. Part: "Level5_P1" | Pos: (10, 29, 85) | Size: (2, 1, 2) | Color: "Bright violet"
2. Part: "Level5_P2" | Pos: (3, 31, 90) | Size: (1.5, 1, 1.5) | Color: "Bright violet"
3. Part: "Level5_P3" | Pos: (-8, 33, 95) | Size: (1.5, 1, 1.5) | Color: "Bright violet"
4. Part: "Level5_P4" | Pos: (0, 35, 100) | Size: (2, 1, 2) | Color: "Bright violet"

LEVEL 6 - Tight Spacing:
1. Part: "Level6_P1" | Pos: (6, 37, 105) | Size: (1.5, 1, 1.5) | Color: "Dark stone grey"
2. Part: "Level6_P2" | Pos: (0, 39, 110) | Size: (1.5, 1, 1.5) | Color: "Dark stone grey"
3. Part: "Level6_P3" | Pos: (-6, 41, 115) | Size: (1.5, 1, 1.5) | Color: "Dark stone grey"

LEVEL 7 - Mixed Heights:
1. Part: "Level7_P1" | Pos: (0, 43, 120) | Size: (1.5, 1, 1.5) | Color: "Really red"
2. Part: "Level7_P2" | Pos: (8, 40, 125) | Size: (1.5, 1, 1.5) | Color: "Really red"
3. Part: "Level7_P3" | Pos: (-8, 45, 130) | Size: (1.5, 1, 1.5) | Color: "Really red"
4. Part: "Level7_P4" | Pos: (0, 47, 135) | Size: (2, 1, 2) | Color: "Really red"

Parent all to Workspace.HighDifficultyObby, Anchored = true"""

    # Step 5: Levels 8-10 (Hard) - extreme difficulty
    prompt5 = """TASK: Build Levels 8-10 (HIGH DIFFICULTY - EXPERT)

Create these extremely challenging platforms:

LEVEL 8 - Micro Platforms:
1. Part: "Level8_P1" | Pos: (10, 49, 140) | Size: (1, 1, 1) | Color: "Really black" | Material: "Glass"
2. Part: "Level8_P2" | Pos: (4, 51, 145) | Size: (1, 1, 1) | Color: "Really black" | Material: "Glass"
3. Part: "Level8_P3" | Pos: (-6, 53, 150) | Size: (1, 1, 1) | Color: "Really black" | Material: "Glass"
4. Part: "Level8_P4" | Pos: (0, 55, 155) | Size: (1, 1, 1) | Color: "Really black" | Material: "Glass"

LEVEL 9 - The Gauntlet:
1. Part: "Level9_P1" | Pos: (12, 57, 160) | Size: (1, 1, 1) | Color: "Hot pink" | Material: "Neon"
2. Part: "Level9_P2" | Pos: (8, 59, 163) | Size: (1, 1, 1) | Color: "Hot pink" | Material: "Neon"
3. Part: "Level9_P3" | Pos: (0, 61, 166) | Size: (1, 1, 1) | Color: "Hot pink" | Material: "Neon"
4. Part: "Level9_P4" | Pos: (-8, 63, 169) | Size: (1, 1, 1) | Color: "Hot pink" | Material: "Neon"
5. Part: "Level9_P5" | Pos: (0, 65, 172) | Size: (1, 1, 1) | Color: "Hot pink" | Material: "Neon"

LEVEL 10 - FINAL CHALLENGE:
1. Part: "Level10_P1" | Pos: (15, 67, 175) | Size: (0.8, 1, 0.8) | Color: "Toothpaste" | Material: "ForceField"
2. Part: "Level10_P2" | Pos: (10, 69, 180) | Size: (0.8, 1, 0.8) | Color: "Toothpaste" | Material: "ForceField"
3. Part: "Level10_P3" | Pos: (0, 71, 185) | Size: (0.8, 1, 0.8) | Color: "Toothpaste" | Material: "ForceField"
4. Part: "Level10_P4" | Pos: (-10, 73, 190) | Size: (0.8, 1, 0.8) | Color: "Toothpaste" | Material: "ForceField"
5. Part: "Level10_P5" | Pos: (0, 75, 195) | Size: (1, 1, 1) | Color: "Toothpaste" | Material: "ForceField"

Parent all to Workspace.HighDifficultyObby, Anchored = true"""

    # Step 6: Create checkpoint system
    prompt6 = """TASK: Create Checkpoint System

Create this EXACT checkpoint script in ServerScriptService:

Script Name: "CheckpointSystem"
Script Type: Script
Parent: ServerScriptService

Source Code:
```lua
local Players = game:GetService("Players")

-- Configuration
local SPAWN_POSITION = Vector3.new(0, 5, 0)

-- Player data storage
local playerCheckpoints = {}

-- Function to set player checkpoint
local function setCheckpoint(player, checkpointPosition)
    playerCheckpoints[player.UserId] = checkpointPosition
    print(player.Name .. " reached checkpoint at " .. tostring(checkpointPosition))
end

-- Respawn player at their checkpoint
local function respawnAtCheckpoint(player)
    local character = player.Character
    if character then
        local humanoidRootPart = character:FindFirstChild("HumanoidRootPart")
        if humanoidRootPart then
            local checkpoint = playerCheckpoints[player.UserId] or SPAWN_POSITION
            humanoidRootPart.CFrame = CFrame.new(checkpoint + Vector3.new(0, 5, 0))
        end
    end
end

-- Player joined
Players.PlayerAdded:Connect(function(player)
    playerCheckpoints[player.UserId] = SPAWN_POSITION
    
    player.CharacterAdded:Connect(function(character)
        local humanoid = character:WaitForChild("Humanoid")
        
        -- Wait a moment then teleport to checkpoint
        wait(0.1)
        respawnAtCheckpoint(player)
        
        -- Death handler
        humanoid.Died:Connect(function()
            wait(2)
            player:LoadCharacter()
        end)
    end)
end)

-- Player left - cleanup
Players.PlayerRemoving:Connect(function(player)
    playerCheckpoints[player.UserId] = nil
end)

print("✅ Checkpoint system initialized!")
```

Create this script exactly as written."""

    # Step 7: Kill parts and death handling
    prompt7 = """TASK: Create Kill Parts System

1. CREATE KILL PART beneath obby:
   - Part Name: "KillPart"
   - Parent: Workspace.HighDifficultyObby
   - Position: Vector3.new(0, -20, 100)
   - Size: Vector3.new(500, 1, 500)
   - BrickColor: "Really red"
   - Material: "Neon"
   - Transparency: 0.5
   - Anchored: true
   - CanCollide: false

2. CREATE DEATH SCRIPT in KillPart:
   Script Name: "DeathScript"
   Script Type: Script
   Parent: Workspace.HighDifficultyObby.KillPart
   
   Source:
```lua
local killPart = script.Parent

killPart.Touched:Connect(function(hit)
    local humanoid = hit.Parent:FindFirstChild("Humanoid")
    if humanoid then
        humanoid.Health = 0
    end
end)
```

Create both the part and the script."""

    # Step 8: Victory system
    prompt8 = """TASK: Create Victory System

1. CREATE VICTORY SCRIPT in FinishPlatform:
   Script Name: "VictoryScript"
   Script Type: Script
   Parent: Workspace.HighDifficultyObby.FinishPlatform
   
   Source:
```lua
local finishPart = script.Parent
local Players = game:GetService("Players")

-- Track who finished
local finishedPlayers = {}

finishPart.Touched:Connect(function(hit)
    local player = Players:GetPlayerFromCharacter(hit.Parent)
    if player and not finishedPlayers[player.UserId] then
        finishedPlayers[player.UserId] = true
        
        -- Victory message
        print(player.Name .. " completed the obby! 🎉")
        
        -- Create victory effect (sparkles)
        local humanoidRootPart = hit.Parent:FindFirstChild("HumanoidRootPart")
        if humanoidRootPart then
            local sparkles = Instance.new("Sparkles")
            sparkles.Parent = humanoidRootPart
            
            -- Teleport back to start after 3 seconds
            wait(3)
            humanoidRootPart.CFrame = CFrame.new(0, 10, 0)
            sparkles:Destroy()
            finishedPlayers[player.UserId] = false
        end
    end
end)
```

Create this script in the FinishPlatform."""

    # Execute prompts in sequence
    prompts = [
        ("1. Clean Workspace", prompt1),
        ("2. Foundation Structure", prompt2),
        ("3. Levels 1-3 (Easy)", prompt3),
        ("4. Levels 4-7 (Medium)", prompt4),
        ("5. Levels 8-10 (Hard)", prompt5),
        ("6. Checkpoint System", prompt6),
        ("7. Kill Parts", prompt7),
        ("8. Victory System", prompt8),
    ]
    
    for step_name, prompt in prompts:
        print(f"\n\n{'#'*80}")
        print(f"# STEP: {step_name}")
        print(f"{'#'*80}")
        
        success = send_prompt_to_robovibe(prompt)
        if not success:
            print(f"❌ Failed at step: {step_name}")
            break
        
        # Wait a bit between steps to let Gemini process
        time.sleep(2)
    
    print("\n\n" + "="*80)
    print("🎉 OBBY BUILD COMPLETE!")
    print("="*80)
    print("\nThe 10-level high-difficulty obby has been created with:")
    print("✅ Progressive difficulty from easy warmup to expert challenges")
    print("✅ Checkpoint system with automatic respawn")
    print("✅ Kill parts for death handling")
    print("✅ Victory celebration at finish line")
    print("✅ Professional color coding and materials")
    print("\nGo test it in Roblox Studio!")

if __name__ == "__main__":
    main()
