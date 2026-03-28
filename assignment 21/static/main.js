const chatBox = document.getElementById("chat-show");
const input = document.getElementById("chat-input");
const sendBtn = document.getElementById("send-btn");

const roomName = "room1"; // dynamic room
const socket = new WebSocket(`ws://${window.location.host}/ws/chat/${roomName}/`);

// connection status
socket.onopen = function (e) {
    console.log("WebSocket connected", e);
};

// Receive message
socket.onmessage = function (e) {
    console.log("Message received:", e.data);
};

// connection error
socket.onerror = function (error) {
    console.log("WebSocket error:", error);
};

// connection close
socket.onclose = function () {
    console.log("WebSocket closed");
};

