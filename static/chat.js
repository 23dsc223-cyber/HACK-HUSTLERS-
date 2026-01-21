function sendMessage() {
    let input = document.getElementById("user-input");
    let message = input.value;
    if (!message) return;

    let chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<div class="user">${message}</div>`;
    input.value = "";

    fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
    })
    .then(res => res.json())
    .then(data => {
        chatBox.innerHTML += `<div class="bot">${data.reply}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    });
}
