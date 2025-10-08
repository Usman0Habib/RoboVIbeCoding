from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
from mcp_client import MCPClient
from gemini_client import GeminiClient
from agentic_engine import AgenticEngine
from file_manager import FileManager

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

mcp_url = os.environ.get('MCP_URL', 'https://jaunita-draughtier-doggedly.ngrok-free.dev')
mcp_client = MCPClient(base_url=mcp_url)
gemini_client = GeminiClient()
file_manager = FileManager()
agentic_engine = AgenticEngine(mcp_client, gemini_client, file_manager)

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    conversation_id = data.get('conversation_id', 'default')
    
    try:
        response = agentic_engine.process_message(user_message, conversation_id)
        file_manager.save_conversation_message(conversation_id, 'user', user_message)
        file_manager.save_conversation_message(conversation_id, 'assistant', response)
        
        return jsonify({
            'success': True,
            'response': response,
            'conversation_id': conversation_id
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stream-chat', methods=['POST'])
def stream_chat():
    data = request.json
    user_message = data.get('message', '')
    conversation_id = data.get('conversation_id', 'default')
    
    def generate():
        try:
            for chunk in agentic_engine.process_message_stream(user_message, conversation_id):
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
            yield f"data: {json.dumps({'done': True})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    from flask import Response
    return Response(generate(), mimetype='text/event-stream')

@app.route('/api/file-tree', methods=['GET'])
def get_file_tree():
    try:
        tree = mcp_client.get_file_tree()
        return jsonify({
            'success': True,
            'tree': tree
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/conversation-history/<conversation_id>', methods=['GET'])
def get_conversation_history(conversation_id):
    try:
        history = file_manager.load_conversation_history(conversation_id)
        return jsonify({
            'success': True,
            'history': history
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'GET':
        settings = file_manager.load_settings()
        settings.pop('gemini_api_key', None)
        settings['gemini_configured'] = gemini_client.configured
        return jsonify({
            'success': True,
            'settings': settings
        })
    else:
        data = request.json
        file_manager.save_settings(data)
        
        if 'gemini_api_key' in data:
            try:
                gemini_client.set_api_key(data['gemini_api_key'])
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 400
        
        if 'mcp_url' in data:
            mcp_client.base_url = data['mcp_url']
        
        return jsonify({
            'success': True,
            'message': 'Settings saved successfully'
        })

@app.route('/api/mcp-status', methods=['GET'])
def mcp_status():
    status = mcp_client.check_connection()
    return jsonify({
        'success': True,
        'connected': status
    })

@app.route('/api/create-backup', methods=['POST'])
def create_backup():
    try:
        backup_path = file_manager.create_backup()
        return jsonify({
            'success': True,
            'backup_path': backup_path
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    os.makedirs('config', exist_ok=True)
    os.makedirs('backups', exist_ok=True)
    os.makedirs('data/conversations', exist_ok=True)
    
    print("🤖 RoboVibeCode - Autonomous Roblox AI Agent")
    print("=" * 50)
    print("Server starting on http://localhost:5000")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
