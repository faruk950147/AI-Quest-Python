const chatBox = document.getElementById("chat-show");
const input = document.getElementById("chat-input");
const sendBtn = document.getElementById("send-btn");

const roomName = "room1"; // dynamic room
const socket = new WebSocket(`ws://${window.location.host}/ws/chat/${roomName}/`);
// Receive message
socket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    chatBox.value += (data.username || "Anonymous") + ": " + data.message + "\n";
};

// Send message
sendBtn.onclick = function () {
    const message = input.value;
    if (!message.trim()) return;

    socket.send(JSON.stringify({
        username: "Faruk",  // replace dynamically if needed
        message: message
    }));

    input.value = "";
};