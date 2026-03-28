const chatBox = document.getElementById("chat-show");
const input = document.getElementById("chat-input");
const sendBtn = document.getElementById("send-btn");

// WebSocket connection
const socket = new WebSocket("ws://" + window.location.host + "/ws/chat/");

// Receive message
socket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    chatBox.value += data.message + "\n";
};

// Send message
sendBtn.onclick = function () {
    const message = input.value;

    socket.send(JSON.stringify({
        'message': message
    }));

    input.value = "";
};