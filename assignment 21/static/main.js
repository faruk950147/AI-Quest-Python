const chatBox = document.getElementById("chat-show");
const input = document.getElementById("chat-input");
const sendBtn = document.getElementById("send-btn");

// Get room name from URL
const roomName = window.location.pathname.split('/')[2];

// Use wss if HTTPS
const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
const socket = new WebSocket(`${protocol}://${window.location.host}/ws/chat/${roomName}/`);

// Connection opened
socket.onopen = function (e) {
    console.log("WebSocket connected:", e);
};

// Message received
socket.onmessage = function (e) {
    console.log("Message received:", e.data);
};

// Connection error
socket.onerror = function (e) {
    console.error("WebSocket error:", e);
};

// connection close
socket.onclose = function () {
    console.log("WebSocket closed");
};

