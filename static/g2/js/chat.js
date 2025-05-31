// static/js/chat.js
document.addEventListener('DOMContentLoaded', () => {
    const messagesUl = document.getElementById('messages');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');

    // Function to update seen status for sent messages
    function updateSeenStatus(messages) {
        messages.forEach(message => {
            const seenIndicator = message.querySelector('.seen-status');
            if (seenIndicator && seenIndicator.classList.contains('pending')) {
                seenIndicator.classList.remove('pending');
            }
        });
    }

    // Function to check if we need a new date separator
    function needsDateSeparator(newMessageDate) {
        const dateSeparators = messagesUl.querySelectorAll('li.date-separator');
        if (dateSeparators.length === 0) return true;
        
        const lastDateSeparator = dateSeparators[dateSeparators.length - 1];
        const lastSeparatorDate = lastDateSeparator.querySelector('span').textContent;
        
        if (lastSeparatorDate === 'Today' && newMessageDate === 'Today') return false;
        return true;
    }

    chatSocket.onopen = () => {
        console.log('WebSocket connected');
        // Update seen status for existing messages
        const sentMessages = messagesUl.querySelectorAll('li.sent');
        updateSeenStatus(sentMessages);
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
            updateSeenStatus(sentMessages);
            return;
        }

        // Regular chat message
        const messageDate = formatMessageDate(data.timestamp);
        
        // Only add date separator if needed
        if (needsDateSeparator(messageDate)) {
            const dateSeparator = document.createElement('li');
            dateSeparator.className = 'date-separator';
            dateSeparator.innerHTML = `<span>${messageDate}</span>`;
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
                ${isMe ? '<span class="seen-status pending"></span>' : ''}
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
  