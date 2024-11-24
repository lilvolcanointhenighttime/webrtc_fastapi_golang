var socket = new WebSocket("ws://localhost:8080/ws");
socket.onmessage = (event) => { console.log(event.data) }
socket.send("hi")