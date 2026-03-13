const socket = new WebSocket("ws://127.0.0.1:8000/chat");

socket.onopen = function() {
    console.log("Connected to chat server");
};

socket.onmessage = function(event) {

    const chat = document.getElementById("chatBox");

    const msg = document.createElement("p");
    msg.innerText = event.data;

    chat.appendChild(msg);
};

function sendMessage(){

    const input = document.getElementById("messageInput");

    socket.send(input.value);

    input.value = "";
}