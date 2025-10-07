let conversationId = 'default';
let isProcessing = false;

marked.setOptions({
    highlight: function(code, lang) {
        if (Prism.languages[lang]) {
            return Prism.highlight(code, Prism.languages[lang], lang);
        }
        return code;
    },
    breaks: true
});

async function checkStatus() {
    try {
        const mcpResponse = await fetch('/api/mcp-status');
        const mcpData = await mcpResponse.json();
        
        const mcpStatus = document.getElementById('mcp-status');
        if (mcpData.connected) {
            mcpStatus.textContent = '🟢 Connected';
            mcpStatus.style.color = 'var(--success-color)';
        } else {
            mcpStatus.textContent = '🔴 Disconnected';
            mcpStatus.style.color = 'var(--error-color)';
        }
        
        const settingsResponse = await fetch('/api/settings');
        const settingsData = await settingsResponse.json();
        
        const geminiStatus = document.getElementById('gemini-status');
        if (settingsData.settings && settingsData.settings.gemini_configured) {
            geminiStatus.textContent = '🟢 Configured';
            geminiStatus.style.color = 'var(--success-color)';
        } else {
            geminiStatus.textContent = '🟡 Not Configured';
            geminiStatus.style.color = 'var(--text-secondary)';
        }
    } catch (error) {
        console.error('Status check failed:', error);
    }
}

async function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    
    if (!message || isProcessing) return;
    
    isProcessing = true;
    const sendBtn = document.getElementById('send-btn');
    const sendBtnText = document.getElementById('send-btn-text');
    sendBtn.disabled = true;
    sendBtnText.textContent = 'Processing...';
    
    input.value = '';
    
    const welcomeMsg = document.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.remove();
    }
    
    addMessage('user', message);
    
    const assistantMessageDiv = addMessage('assistant', '');
    const messageContent = assistantMessageDiv.querySelector('.message-content');
    
    try {
        const response = await fetch('/api/stream-chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                conversation_id: conversationId
            })
        });
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        let fullResponse = '';
        
        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            
            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop();
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        const data = JSON.parse(line.slice(6));
                        if (data.chunk) {
                            fullResponse += data.chunk;
                            messageContent.innerHTML = marked.parse(fullResponse);
                            Prism.highlightAllUnder(messageContent);
                            scrollToBottom();
                        } else if (data.error) {
                            fullResponse += `\n\n❌ Error: ${data.error}`;
                            messageContent.innerHTML = marked.parse(fullResponse);
                        }
                    } catch (e) {
                        console.error('Parse error:', e);
                    }
                }
            }
        }
        
    } catch (error) {
        messageContent.innerHTML = marked.parse(`❌ Error: ${error.message}`);
    }
    
    isProcessing = false;
    sendBtn.disabled = false;
    sendBtnText.textContent = 'Send';
    scrollToBottom();
}

function addMessage(role, content) {
    const chatContainer = document.getElementById('chat-container');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = role === 'user' ? '👤' : '🤖';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    if (content) {
        messageContent.innerHTML = marked.parse(content);
        setTimeout(() => {
            Prism.highlightAllUnder(messageContent);
        }, 0);
    } else {
        messageContent.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';
    }
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);
    chatContainer.appendChild(messageDiv);
    
    scrollToBottom();
    return messageDiv;
}

function scrollToBottom() {
    const chatContainer = document.getElementById('chat-container');
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function openSettings() {
    const modal = document.getElementById('settings-modal');
    modal.classList.add('active');
    
    fetch('/api/settings')
        .then(res => res.json())
        .then(data => {
            if (data.settings) {
                document.getElementById('mcp-url').value = data.settings.mcp_url || 'http://localhost:3002';
                document.getElementById('theme-select').value = data.settings.theme || 'dark';
            }
        });
}

function closeSettings() {
    const modal = document.getElementById('settings-modal');
    modal.classList.remove('active');
}

async function saveSettings() {
    const geminiApiKey = document.getElementById('gemini-api-key').value;
    const mcpUrl = document.getElementById('mcp-url').value;
    const theme = document.getElementById('theme-select').value;
    
    const settings = {
        mcp_url: mcpUrl,
        theme: theme
    };
    
    if (geminiApiKey) {
        settings.gemini_api_key = geminiApiKey;
    }
    
    try {
        const response = await fetch('/api/settings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(settings)
        });
        
        const data = await response.json();
        if (data.success) {
            closeSettings();
            checkStatus();
            alert('Settings saved successfully!');
        }
    } catch (error) {
        alert('Failed to save settings: ' + error.message);
    }
}

async function toggleFileTree() {
    const container = document.getElementById('file-tree-container');
    const fileTreeDiv = document.getElementById('file-tree');
    
    if (container.style.display === 'none') {
        container.style.display = 'block';
        fileTreeDiv.innerHTML = '<p class="loading">Loading...</p>';
        
        try {
            const response = await fetch('/api/file-tree');
            const data = await response.json();
            
            if (data.success && data.tree) {
                fileTreeDiv.innerHTML = `<pre>${JSON.stringify(data.tree, null, 2)}</pre>`;
            } else {
                fileTreeDiv.innerHTML = '<p style="color: var(--error-color);">Failed to load file tree</p>';
            }
        } catch (error) {
            fileTreeDiv.innerHTML = `<p style="color: var(--error-color);">Error: ${error.message}</p>`;
        }
    } else {
        container.style.display = 'none';
    }
}

async function createBackup() {
    try {
        const response = await fetch('/api/create-backup', {
            method: 'POST'
        });
        const data = await response.json();
        
        if (data.success) {
            alert('Backup created successfully at: ' + data.backup_path);
        } else {
            alert('Failed to create backup: ' + data.error);
        }
    } catch (error) {
        alert('Error creating backup: ' + error.message);
    }
}

function newConversation() {
    conversationId = 'conv_' + Date.now();
    const chatContainer = document.getElementById('chat-container');
    chatContainer.innerHTML = `
        <div class="welcome-message">
            <h2>👋 New Conversation Started</h2>
            <p>Ready to build something amazing in Roblox Studio!</p>
        </div>
    `;
}

async function reconnectMCP() {
    const mcpStatus = document.getElementById('mcp-status');
    mcpStatus.textContent = '🔄 Connecting...';
    mcpStatus.style.color = 'var(--text-secondary)';
    
    try {
        const response = await fetch('/api/mcp-status');
        const data = await response.json();
        
        if (data.connected) {
            mcpStatus.textContent = '🟢 Connected';
            mcpStatus.style.color = 'var(--success-color)';
            alert('Successfully connected to MCP server!');
        } else {
            mcpStatus.textContent = '🔴 Disconnected';
            mcpStatus.style.color = 'var(--error-color)';
            alert('Failed to connect to MCP server. Make sure it is running on the configured URL.');
        }
    } catch (error) {
        mcpStatus.textContent = '🔴 Disconnected';
        mcpStatus.style.color = 'var(--error-color)';
        alert('Error connecting to MCP server: ' + error.message);
    }
}

document.getElementById('user-input').addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

window.addEventListener('click', (e) => {
    const modal = document.getElementById('settings-modal');
    if (e.target === modal) {
        closeSettings();
    }
});

checkStatus();
setInterval(checkStatus, 10000);
