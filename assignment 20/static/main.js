// web socket
var socket = new WebSocket("ws://127.0.0.1:8000/ws/office/");

socket.onopen = function (e) {
    console.log("Connected to WebSocket server");
    socket.send("Hello Server!");
};

socket.onmessage = function (event) {
    console.log("Message from server:", event.data);
    socket.send("Hello Server!");
};

socket.onclose = function (event) {
    console.log("Connection closed");
};

socket.onerror = function (error) {
    console.log("Error:", error);
};

