# RoboVibeCode - Autonomous Roblox AI Agent

## Overview
RoboVibeCode is a complete, fully autonomous AI agent system specifically designed for Roblox Studio development. It operates like Replit Agent 3 but is specialized for creating Roblox games through natural language commands. The system enables "vibecoding" - autonomous development without human intervention.

## Project Purpose
- Enable autonomous Roblox game development through AI
- Provide a chat-based interface for natural language game creation
- Integrate with existing MCP (Model Context Protocol) server for Roblox Studio operations
- Generate complete game systems, scripts, and features automatically
- Support multiple game genres (Obby, Tycoon, RPG, Simulator, etc.)

## Current State
✅ **COMPLETED MVP** - Fully functional autonomous AI agent for Roblox Studio
- Web-based chat interface with real-time streaming responses
- Google Gemini AI integration for natural language understanding
- MCP client for Roblox Studio communication
- Autonomous task planning and execution engine
- Roblox-specific knowledge base with Lua code generation
- Local file storage for conversation history and backups
- Modern dark theme UI with code syntax highlighting

## Technology Stack

### Backend (Python)
- **Flask** - Web server and API endpoints
- **Google Generative AI** - Gemini Pro for AI responses
- **Requests** - HTTP client for MCP communication
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **HTML5/CSS3/JavaScript** - Modern web interface
- **Marked.js** - Markdown rendering for formatted responses
- **Prism.js** - Code syntax highlighting (Lua support)
- **Server-Sent Events** - Real-time streaming responses

## Project Architecture

```
RoboVibeCode/
├── backend/
│   ├── app.py                 # Flask server & API routes
│   ├── mcp_client.py          # MCP server communication
│   ├── gemini_client.py       # Google Gemini AI integration
│   ├── agentic_engine.py      # Autonomous planning & execution
│   ├── roblox_knowledge.py    # Roblox-specific knowledge base
│   └── file_manager.py        # Local storage & backups
├── frontend/
│   ├── index.html             # Main chat interface
│   ├── style.css              # Modern dark theme styling
│   └── script.js              # Real-time communication
├── config/                    # Settings (API keys, preferences)
├── data/                      # Conversation history
└── backups/                   # Project snapshots
```

## Core Features

### 1. Autonomous Planning Engine
- Analyzes user requests and creates execution plans
- Breaks down complex tasks into actionable steps
- Adapts dynamically to errors and changing requirements
- Provides real-time progress updates

### 2. MCP Integration
Connects to localhost:3002 for Roblox Studio operations:
- `get_file_tree` - Project structure analysis
- `read_file` / `write_file` - Script editing
- `create_script` - New script generation
- `create_roblox_objects` - Object creation
- `modify_object_properties` - Property editing
- `move_file` / `delete_file` - File organization

### 3. Roblox Expertise
- Deep knowledge of Roblox services and architecture
- Lua code generation with best practices
- Script type understanding (Script, LocalScript, ModuleScript)
- Remote communication patterns (RemoteEvent, RemoteFunction)
- DataStore implementation for persistence
- Security best practices (server validation)

### 4. Game Templates
Supports automatic generation of:
- **Obby** - Obstacle courses with checkpoints
- **Tycoon** - Money systems and upgrades
- **RPG** - Inventory, quests, combat
- **Simulator** - Click/idle game mechanics

### 5. Local Storage System
- Conversation history saved as JSON
- Timestamped backups before major changes
- Settings persistence (API keys, preferences)
- No external database required

## How to Use

### Setup
1. Start the server: Already running on port 5000
2. Open web interface at http://localhost:5000
3. Configure Gemini API key in Settings (free tier from Google AI Studio)
4. Ensure MCP server is running on localhost:3002

### Example Commands
- "Create an obby game with 20 levels and a leaderboard"
- "Add a script to handle player checkpoints"
- "Show me the current project structure"
- "Build a tycoon system with money and upgrades"
- "Analyze my project and suggest optimizations"

### Features Available
- ⚙️ **Settings** - Configure API keys and preferences
- 💾 **Create Backup** - Save project snapshots
- 📁 **Project Files** - View Roblox Studio structure
- ➕ **New Chat** - Start fresh conversation

## API Endpoints

- `POST /api/chat` - Send message and get response
- `POST /api/stream-chat` - Streaming response with SSE
- `GET /api/file-tree` - Get Roblox project structure
- `GET /api/conversation-history/:id` - Load conversation
- `GET/POST /api/settings` - Manage settings
- `GET /api/mcp-status` - Check MCP connection
- `POST /api/create-backup` - Create project backup

## Configuration

All settings stored in `config/settings.json`:
- `gemini_api_key` - Google Gemini API key
- `mcp_url` - MCP server URL (default: localhost:3002)
- `theme` - UI theme (dark/light)

## Recent Changes (October 7, 2025)
- ✅ Created complete backend infrastructure with Flask
- ✅ Implemented MCP client for Roblox Studio integration
- ✅ Integrated Google Gemini AI with streaming support
- ✅ Built autonomous planning and execution engine
- ✅ Added Roblox-specific knowledge base with code templates
- ✅ Created modern web-based chat interface
- ✅ Implemented local file storage and backup system
- ✅ Added real-time status monitoring for MCP and Gemini
- ✅ Configured workflow for automatic server startup

## User Preferences
- **Cost Constraint**: Everything must be completely free (no paid services)
- **Platform**: Windows-optimized, web-based for cross-compatibility
- **Storage**: Local file storage only, no external databases
- **Integration**: MCP server at localhost:3002 for Roblox Studio
- **AI Provider**: Google Gemini (free tier)

## Next Phase Features
These advanced features can be added in future iterations:
- Game genre templates with automatic generation
- Bulk script operations and mass refactoring
- Advanced asset management with dependency mapping
- Performance analysis and security scanning
- Multi-step rollback system with visual diffs
- Long-running autonomous mode with adaptive error recovery
