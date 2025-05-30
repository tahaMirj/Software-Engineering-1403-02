// static/js/chat.js
document.addEventListener('DOMContentLoaded', () => {
    const messagesUl = document.getElementById('messages');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    let lastMessageDate = null;
  
    // Initialize lastMessageDate from existing messages
    const existingMessages = messagesUl.querySelectorAll('li');
    if (existingMessages.length > 0) {
      const lastMessage = existingMessages[existingMessages.length - 1];
      const timestamp = lastMessage.querySelector('.timestamp').title;
      lastMessageDate = new Date(timestamp).toDateString();
    }

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
  
      // Get the current message's date
      const messageDate = new Date(data.timestamp).toDateString();

      // Check if this is the first message of a new day
      if (messageDate !== lastMessageDate) {
        const dateSeparator = document.createElement('div');
        dateSeparator.className = 'date-separator';
        dateSeparator.innerHTML = `<span>${formatMessageDate(data.timestamp)}</span>`;
        messagesUl.appendChild(dateSeparator);
        lastMessageDate = messageDate;
      }

      // Create and append the message
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
        })}">${formatTime(data.timestamp)}</div>
      `;
      messagesUl.appendChild(li);
      
      // Scroll to the bottom
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
  