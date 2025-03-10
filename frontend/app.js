/chat-app/frontend/app.js

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatDisplay = document.getElementById('chat-display');

    form.addEventListener('submit', async function(event) {
        event.preventDefault();
        const message = messageInput.value.trim();
        if (message === '') return;

        // Display the message in the chat display
        const messageElement = document.createElement('div');
        messageElement.textContent = `You: ${message}`;
        chatDisplay.appendChild(messageElement);

        // Send the message to the backend for moderation
        try {
            const response = await fetch('YOUR_API_GATEWAY_URL', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });

            const result = await response.json();
            const moderationResult = result.moderationResult;

            // Display the moderation result
            const moderationElement = document.createElement('div');
            moderationElement.textContent = `Moderation: ${moderationResult}`;
            chatDisplay.appendChild(moderationElement);
        } catch (error) {
            console.error('Error:', error);
            const errorElement = document.createElement('div');
            errorElement.textContent = 'Error: Unable to moderate message';
            chatDisplay.appendChild(errorElement);
        }

        // Clear the input field
        messageInput.value = '';
    });
});