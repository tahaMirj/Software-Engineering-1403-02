document.addEventListener('DOMContentLoaded', () => {
    const messagesUl = document.getElementById('messages');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const blockBtn = document.getElementById('block-button');

    let chatIsBlocked = false;

    const chatSocket = new WebSocket(
        (window.location.protocol === "https:" ? "wss" : "ws") + '://' +
        window.location.host + '/ws/chat/' + otherUsername + '/'
    );

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function updateChatUI(isBlocked, isBlocker) {
        console.log("updateChatUI" + isBlocked + isBlocker)
        chatIsBlocked = isBlocked;
        chatInput.disabled = isBlocked;
        chatForm.querySelector('button[type="submit"]').disabled = isBlocked;

        if (isBlocked) {
            if (isBlocker) {
                blockBtn.textContent = 'Unblock';
                blockBtn.disabled = false;
                blockBtn.onclick = sendUnblock;
            } else {
                blockBtn.textContent = 'Blocked';
                blockBtn.disabled = true;
            }
        } else {
            blockBtn.textContent = 'Block';
            blockBtn.disabled = false;
            blockBtn.onclick = sendBlock;
        }
    }

    function sendBlock() {
        fetch('/group2/api/v1/block/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ username: otherUsername })
        })
        .then(res => {
            if (!res.ok) throw new Error('Block failed');
            return res.json();
        })
        .then(() => {
            chatSocket.send(JSON.stringify({ action: 'refresh_state' }));
            // updateChatUI(true, true);
        })
        .catch(err => alert(err.message));
    }

    function sendUnblock() {
        fetch('/group2/api/v1/unblock/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ username: otherUsername })
        })
        .then(res => {
            if (!res.ok) throw new Error('Unblock failed');
            return res.json();
        })
        .then(() => {
            chatSocket.send(JSON.stringify({ action: 'refresh_state' }));
            // updateChatUI(false, false);
        })
        .catch(err => alert(err.message));
    }

    // blockBtn.id = 'chat-block';
    blockBtn.onclick = sendBlock;

    function updateSeenStatus(messages) {
        messages.forEach(message => {
            const seenIndicator = message.querySelector('.seen-status');
            if (seenIndicator && seenIndicator.classList.contains('pending')) {
                seenIndicator.classList.remove('pending');
            }
        });
    }

    function needsDateSeparator(newMessageDate) {
        const dateSeparators = messagesUl.querySelectorAll('li.date-separator');
        if (dateSeparators.length === 0) return true;
        
        const lastDateSeparator = dateSeparators[dateSeparators.length - 1];
        const lastSeparatorDate = lastDateSeparator.querySelector('span').textContent;
        
        return !(lastSeparatorDate === 'Today' && newMessageDate === 'Today');
    }

    function formatMessageDate(timestamp) {
        const date = new Date(timestamp);
        const today = new Date();
        return date.toDateString() === today.toDateString()
            ? 'Today'
            : date.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
    }

    function formatTime(timestamp) {
        return new Date(timestamp).toLocaleTimeString('en-US', { 
            hour: 'numeric', 
            minute: '2-digit', 
            hour12: true 
        });
    }

    chatSocket.onopen = () => {
        console.log('WebSocket connected');
        const sentMessages = messagesUl.querySelectorAll('li.sent');
        updateSeenStatus(sentMessages);
    };

    const socketMessageHandlers = {
        redirect: (data) => {
            window.location.href = data.url;
        },
        error: (data) => {
            alert(data.message);
        },
        connection_established: (data) => {
            console.log(data.message);
        },
        messages_seen: (data) => {
            const sentMessages = messagesUl.querySelectorAll('li.sent');
            updateSeenStatus(sentMessages);
        },
        // chat_blocked: (data) => {
        //     const isBlocker = data.blocked_by === currentUsername;
        //     updateChatUI(true, isBlocker);
        // },
        // chat_unblocked: (data) => {
        //     updateChatUI(false, false);
        // },
        update_state: (data) => {
            updateChatUI(data.blocked, data.blocked_by === currentUsername);
        },
        chat_message: (data) => {
            // if (chatIsBlocked) return;

            const messageDate = formatMessageDate(data.timestamp);
            if (needsDateSeparator(messageDate)) {
                const dateSeparator = document.createElement('li');
                dateSeparator.className = 'date-separator';
                dateSeparator.innerHTML = `<span>${messageDate}</span>`;
                messagesUl.appendChild(dateSeparator);
            }

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
        }
    };

    chatSocket.onmessage = (e) => {
        const data = JSON.parse(e.data);
        try{
            const handler = socketMessageHandlers[data.type];
            handler(data);
        } catch {
            console.log("FUCK" + JSON.stringify(data));
        }
    };

    chatSocket.onclose = () => {
        console.log('WebSocket closed');
    };

    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const msg = chatInput.value.trim();
        if (!msg || chatIsBlocked) return;
        chatSocket.send(JSON.stringify({ message: msg }));
        chatInput.value = '';
    });
});
