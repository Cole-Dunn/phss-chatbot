/**
 * Chatbot Widget JavaScript
 * Handles user interactions and communication with the RAG backend
 */

class ChatbotWidget {
    constructor() {
        // Configuration
        this.apiUrl = 'http://localhost:8000';  // Change this to your deployed backend URL
        this.conversationHistory = [];
        
        // DOM elements
        this.chatToggle = document.getElementById('chat-toggle');
        this.chatWidget = document.getElementById('chat-widget');
        this.chatClose = document.getElementById('chat-close');
        this.chatMessages = document.getElementById('chat-messages');
        this.chatInput = document.getElementById('chat-input');
        this.sendButton = document.getElementById('send-button');
        this.typingIndicator = document.getElementById('typing-indicator');
        
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Toggle chat widget
        this.chatToggle.addEventListener('click', () => this.openChat());
        this.chatClose.addEventListener('click', () => this.closeChat());
        
        // Send message events
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Input validation
        this.chatInput.addEventListener('input', () => {
            this.sendButton.disabled = this.chatInput.value.trim().length === 0;
        });
    }

    openChat() {
        this.chatWidget.classList.add('open');
        this.chatToggle.style.display = 'none';
        this.chatInput.focus();
    }

    closeChat() {
        this.chatWidget.classList.remove('open');
        this.chatToggle.style.display = 'flex';
    }

    async sendMessage() {
        const message = this.chatInput.value.trim();
        if (!message) return;

        // Add user message to chat
        this.addMessage(message, 'user');
        this.chatInput.value = '';
        this.sendButton.disabled = true;

        // Show typing indicator
        this.showTypingIndicator();

        try {
            // Send to backend
            const response = await fetch(`${this.apiUrl}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    conversation_history: this.conversationHistory
                })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            
            // Hide typing indicator
            this.hideTypingIndicator();
            
            // Add bot response to chat
            this.addMessage(data.response, 'bot', data.sources);
            
            // Update conversation history
            this.conversationHistory.push(
                { role: 'user', content: message },
                { role: 'assistant', content: data.response }
            );
            
            // Keep only last 8 messages (4 exchanges) for context
            if (this.conversationHistory.length > 8) {
                this.conversationHistory = this.conversationHistory.slice(-8);
            }

        } catch (error) {
            console.error('Error sending message:', error);
            this.hideTypingIndicator();
            this.addMessage(
                'Sorry, I encountered an error. Please try again later or contact support.',
                'bot'
            );
        }
    }

    addMessage(text, sender, sources = []) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        const textDiv = document.createElement('div');
        textDiv.className = 'message-text';
        textDiv.textContent = text;
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = this.getCurrentTime();
        
        contentDiv.appendChild(textDiv);
        
        // Add sources if provided
        if (sources && sources.length > 0) {
            const sourcesDiv = document.createElement('div');
            sourcesDiv.className = 'message-sources';
            sourcesDiv.innerHTML = `
                <small style="color: #666; font-size: 11px;">
                    📚 Sources: ${sources.join(', ')}
                </small>
            `;
            contentDiv.appendChild(sourcesDiv);
        }
        
        contentDiv.appendChild(timeDiv);
        messageDiv.appendChild(contentDiv);
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    showTypingIndicator() {
        this.typingIndicator.style.display = 'flex';
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        this.typingIndicator.style.display = 'none';
    }

    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }

    getCurrentTime() {
        return new Date().toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
        });
    }
}

// Initialize chatbot when page loads
document.addEventListener('DOMContentLoaded', function() {
    new ChatbotWidget();
});

// Handle potential errors
window.addEventListener('error', function(e) {
    console.error('Chatbot widget error:', e.error);
});