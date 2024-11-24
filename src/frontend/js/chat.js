const socket = new WebSocket("ws://" + window.location.host + "/api/v2/ws");

socket.onopen = () => {
    console.log("Соединение установлено");
};

socket.onmessage = (event) => {
    const messagesDiv = document.getElementById('messages');
    answer = JSON.parse(event.data);
    messagesDiv.innerHTML += `<p>${answer.body}</p>`;
};

socket.onclose = () => {
    console.log("Соединение закрыто");
};

const form = document.getElementById('dataForm');
form.addEventListener('submit', (event) => {
    event.preventDefault();

    const inputData = document.getElementById('dataInput').value;
    socket.send(inputData);

    document.getElementById('dataInput').value = '';
});
