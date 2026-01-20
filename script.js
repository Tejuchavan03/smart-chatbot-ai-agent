function sendMessage() {
    let input = document.getElementById("userInput");
    let message = input.value;
    if (message === "") return;

    let chat = document.getElementById("chat");
    chat.innerHTML += `<div class='user'>You: ${message}</div>`;
    input.value = "";

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        chat.innerHTML += `<div class='bot'>Bot: ${data.reply}</div>`;
        chat.scrollTop = chat.scrollHeight;
    });
}
