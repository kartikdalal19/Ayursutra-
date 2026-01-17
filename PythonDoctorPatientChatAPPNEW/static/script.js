const socket = io();

let currentRoom = null;

// Receive chat history when joining a room
socket.on('chat_history', history => {
    const chatBox = document.getElementById('chatBox');
    chatBox.innerHTML = '';  // Clear old messages

    history.forEach(entry => {
        const p = document.createElement('p');
        p.innerHTML = `<b>${entry.user}:</b> ${entry.msg}`;
        chatBox.appendChild(p);
    });
    chatBox.scrollTop = chatBox.scrollHeight;
});

socket.on('status', data => {
    const chatBox = document.getElementById('chatBox');
    const p = document.createElement('p');
    p.style.fontStyle = 'italic';
    p.textContent = data.msg;
    chatBox.appendChild(p);
    chatBox.scrollTop = chatBox.scrollHeight;
});

socket.on('message', data => {
    const chatBox = document.getElementById('chatBox');
    const p = document.createElement('p');
    p.innerHTML = `<b>${data.user}:</b> ${data.msg}`;
    chatBox.appendChild(p);
    chatBox.scrollTop = chatBox.scrollHeight;
});

function joinRoom(room, contactName) {
    if (currentRoom) {
        socket.emit('leave', { room: currentRoom });
    }
    currentRoom = room;
    socket.emit('join', { room: currentRoom });

    document.getElementById('roomTitle').textContent = 'Chat with ' + contactName;
    document.getElementById('messageInput').disabled = false;
    document.getElementById('sendBtn').disabled = false;

    // Clear chat box (history will be loaded by event)
    document.getElementById('chatBox').innerHTML = '';
}

function sendMessage() {
    const input = document.getElementById('messageInput');
    const msg = input.value.trim();
    if (!msg || !currentRoom) return;

    socket.emit('message', { room: currentRoom, msg: msg });
    input.value = '';
}
