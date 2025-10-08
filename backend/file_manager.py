import json
import os
from datetime import datetime
import shutil

class FileManager:
    def __init__(self):
        self.config_dir = 'config'
        self.data_dir = 'data'
        self.backup_dir = 'backups'
        self.conversations_dir = os.path.join(self.data_dir, 'conversations')
        
        os.makedirs(self.config_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
        os.makedirs(self.conversations_dir, exist_ok=True)
    
    def load_settings(self):
        settings_path = os.path.join(self.config_dir, 'settings.json')
        if os.path.exists(settings_path):
            with open(settings_path, 'r') as f:
                return json.load(f)
        return {
            'theme': 'dark',
            'mcp_url': 'https://jaunita-draughtier-doggedly.ngrok-free.dev',
            'gemini_api_key': ''
        }
    
    def save_settings(self, settings):
        settings_path = os.path.join(self.config_dir, 'settings.json')
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=2)
    
    def load_conversation_history(self, conversation_id):
        conv_path = os.path.join(self.conversations_dir, f'{conversation_id}.json')
        if os.path.exists(conv_path):
            with open(conv_path, 'r') as f:
                return json.load(f)
        return []
    
    def save_conversation_message(self, conversation_id, role, content):
        conv_path = os.path.join(self.conversations_dir, f'{conversation_id}.json')
        
        history = self.load_conversation_history(conversation_id)
        history.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
        
        with open(conv_path, 'w') as f:
            json.dump(history, f, indent=2)
    
    def create_backup(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'backup_{timestamp}'
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        os.makedirs(backup_path, exist_ok=True)
        
        if os.path.exists(self.data_dir):
            shutil.copytree(self.data_dir, os.path.join(backup_path, 'data'))
        
        if os.path.exists(self.config_dir):
            shutil.copytree(self.config_dir, os.path.join(backup_path, 'config'))
        
        manifest = {
            'timestamp': timestamp,
            'created': datetime.now().isoformat(),
            'type': 'automatic'
        }
        
        with open(os.path.join(backup_path, 'manifest.json'), 'w') as f:
            json.dump(manifest, f, indent=2)
        
        return backup_path
    
    def list_backups(self):
        if not os.path.exists(self.backup_dir):
            return []
        
        backups = []
        for item in os.listdir(self.backup_dir):
            backup_path = os.path.join(self.backup_dir, item)
            if os.path.isdir(backup_path):
                manifest_path = os.path.join(backup_path, 'manifest.json')
                if os.path.exists(manifest_path):
                    with open(manifest_path, 'r') as f:
                        manifest = json.load(f)
                        backups.append({
                            'name': item,
                            'path': backup_path,
                            'timestamp': manifest.get('timestamp'),
                            'created': manifest.get('created')
                        })
        
        return sorted(backups, key=lambda x: x['timestamp'], reverse=True)
