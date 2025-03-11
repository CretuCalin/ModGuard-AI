document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatDisplay = document.getElementById('chat-display');

    const moderationChecks = {
        cyberbullying: document.getElementById('cyberbullying'),
        ageAppropriate: document.getElementById('age-appropriate'),
        personalInfo: document.getElementById('personal-info'),
        strangerDanger: document.getElementById('stranger-danger'),
        languageFilter: document.getElementById('language-filter'),
        positiveCommunication: document.getElementById('positive-communication')
    };

    if (!form || !messageInput || !chatDisplay) {
        console.error('Required elements are missing in the DOM');
        return;
    }

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
            const response = await fetch('https://your-lambda-function-url', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });
            const result = await response.json();

            // Update moderation checks
            updateModerationChecks(result);
        } catch (error) {
            console.error('Error during moderation:', error);
        }

        messageInput.value = '';
    });

    function updateModerationChecks(result) {
        moderationChecks.cyberbullying.className = result.cyberbullying ? 'red' : 'green';
        moderationChecks.ageAppropriate.className = result.ageAppropriate ? 'red' : 'green';
        moderationChecks.personalInfo.className = result.personalInfo ? 'red' : 'green';
        moderationChecks.strangerDanger.className = result.strangerDanger ? 'red' : 'green';
        moderationChecks.languageFilter.className = result.languageFilter ? 'red' : 'green';
        moderationChecks.positiveCommunication.className = result.positiveCommunication ? 'red' : 'green';
    }
});