// static/js/chat.js
document.addEventListener('DOMContentLoaded', () => {
    const messagesUl = document.getElementById('messages');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');

    chatSocket.onopen = () => {
        console.log('WebSocket connected');
    };

    chatSocket.onmessage = (e) => {
        const data = JSON.parse(e.data);

        if (data.type === 'redirect') {
            window.location.href = data.url;
            return;
        }
        if (data.type === 'error') {
            alert(data.message);
            return;
        }
        if (data.type === 'connection_established') {
            console.log(data.message);
            return;
        }
        if (data.type === 'messages_seen') {
            // Update seen status for all messages from the current user
            const sentMessages = messagesUl.querySelectorAll('li.sent');
            sentMessages.forEach(message => {
                const seenIndicator = message.querySelector('.seen-status');
                if (!seenIndicator) {
                    const timestamp = message.querySelector('.timestamp');
                    const seenSpan = document.createElement('span');
                    seenSpan.className = 'seen-status';
                    seenSpan.textContent = '✓';
                    timestamp.appendChild(seenSpan);
                }
            });
            return;
        }

        // Regular chat message
        const messageDate = new Date(data.timestamp).toDateString();
        const lastMessage = messagesUl.lastElementChild;
        const lastMessageDate = lastMessage ? 
            new Date(lastMessage.querySelector('.timestamp').title).toDateString() : null;

        // Add date separator if it's a new day
        if (messageDate !== lastMessageDate) {
            const dateSeparator = document.createElement('li');
            dateSeparator.className = 'date-separator';
            dateSeparator.innerHTML = `<span>${formatMessageDate(data.timestamp)}</span>`;
            messagesUl.appendChild(dateSeparator);
        }

        // Create the message element
        const li = document.createElement('li');
        const isMe = data.sender_username === currentUsername;
        li.classList.add(isMe ? 'sent' : 'received');
        
        li.innerHTML = `
            <div class="meta">${data.sender_username}</div>
            <div class="message-content">${data.message}</div>
            <div class="timestamp" title="${new Date(data.timestamp).toLocaleString('en-US', {
                month: 'long',
                day: 'numeric',
                year: 'numeric',
                hour: 'numeric',
                minute: '2-digit',
                hour12: true
            })}">
                ${formatTime(data.timestamp)}
                ${isMe ? '<span class="seen-status pending">✓</span>' : ''}
            </div>
        `;
        messagesUl.appendChild(li);
        messagesUl.scrollTop = messagesUl.scrollHeight;
    };

    chatSocket.onclose = () => {
        console.log('WebSocket closed');
    };

    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const msg = chatInput.value.trim();
        if (!msg) return;
        chatSocket.send(JSON.stringify({ message: msg }));
        chatInput.value = '';
    });
});
  