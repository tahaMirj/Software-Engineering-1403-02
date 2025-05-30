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
  
      // it's a chat message
      const li = document.createElement('li');
      const isMe = data.sender_username === "{{ user.username }}";
      li.classList.add(isMe ? 'sent' : 'received');
      li.innerHTML = `
        ${data.message}
        <div class="meta">${data.sender_username} • ${new Date(data.timestamp).toLocaleTimeString()}</div>
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
  