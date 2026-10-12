
document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("chat-toggle");
    const widget = document.getElementById("chat-widget");
    const close = document.getElementById("chat-close");
    const toggleIcon = document.getElementById("toggle-icon");

    const form = document.getElementById("chat-form");
    const input = document.getElementById("chat-input");
    const sendButton = document.getElementById("send-button");
    const messages = document.getElementById("chat-messages");

    let isSending = false;

    function openChat() {
        widget.hidden = false;
        toggle.setAttribute("aria-expanded", "true");
        toggleIcon.textContent = "×";
        input.focus();
    }

    function closeChat() {
        widget.hidden = true;
        toggle.setAttribute("aria-expanded", "false");
        toggleIcon.textContent = "✦";
    }

    toggle.addEventListener("click", () => {
        if (widget.hidden) {
            openChat();
        } else {
            closeChat();
        }
    });

    close.addEventListener("click", closeChat);

    function addMessage(text, sender) {
        const message = document.createElement("div");
        message.className =
            "message " +
            (sender === "user" ? "user-message" : "bot-message");

        const bubble = document.createElement("div");
        bubble.className = "bubble";
        bubble.textContent = text;

        const time = document.createElement("span");
        time.className = "message-time";
        time.textContent = sender === "user" ? "You" : "Assistant";

        message.append(bubble, time);
        messages.appendChild(message);
        messages.scrollTop = messages.scrollHeight;
    }

    async function sendMessage(rawMessage) {
        const message = rawMessage.trim();

        if (!message || isSending) return;

        if (message.length > 1000) {
            addMessage("Please keep your message under 1000 characters.", "bot");
            return;
        }

        isSending = true;
        input.disabled = true;
        sendButton.disabled = true;

        addMessage(message, "user");
        input.value = "";

        const typing = document.createElement("div");
        typing.className = "typing";
        typing.textContent = "Assistant is typing...";
        messages.appendChild(typing);
        messages.scrollTop = messages.scrollHeight;

        try {
            const response = await fetch("/api/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message })
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(data.reply || "Request failed.");
            }

            addMessage(data.reply, "bot");

        } catch (error) {
            addMessage(
                "I couldn't connect to the assistant. Please try again or contact our team on WhatsApp.",
                "bot"
            );
            console.error("Chat error:", error);

        } finally {
            typing.remove();
            isSending = false;
            input.disabled = false;
            sendButton.disabled = false;

            if (!widget.hidden) input.focus();
        }
    }

    form.addEventListener("submit", event => {
        event.preventDefault();
        sendMessage(input.value);
    });

    messages.addEventListener("click", event => {
        const button = event.target.closest("button[data-message]");
        if (button) {
            sendMessage(button.dataset.message);
        }
    });

    document.addEventListener("keydown", event => {
        if (event.key === "Escape" && !widget.hidden) {
            closeChat();
        }
    });

    console.log("Park Lane Motors chatbot loaded successfully.");
});
