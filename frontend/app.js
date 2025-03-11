document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatDisplay = document.getElementById('chat-display');

    const moderationChecks = {
        cyberbullying: document.getElementById('cyberbullying'),
        notAgeAppropriate: document.getElementById('age-appropriate'),
        personalInfo: document.getElementById('personal-info'),
        strangerDanger: document.getElementById('stranger-danger'),
        languageFilter: document.getElementById('language-filter'),
        negativeCommunication: document.getElementById('positive-communication')
    };

    var elems = document.querySelectorAll('.tooltipped');
    var instances = M.Tooltip.init(elems);

    if (!form || !messageInput || !chatDisplay) {
        console.error('Required elements are missing in the DOM');
        return;
    }

    form.addEventListener('submit', async function(event) {
        event.preventDefault();

        document.getElementById('chat-form').addEventListener('submit', function(event) {
            event.preventDefault();
            const spinner = document.getElementById('loading-spinner');
            spinner.style.display = 'block';
        
            // Simulate a moderation response delay
            setTimeout(() => {
                spinner.style.display = 'none';
                // Handle the moderation response here
            }, 2000); // Replace with actual moderation response handling
        });

        const message = messageInput.value.trim();
        if (message === '') return;

        // Display the message in the chat display
        const messageElement = document.createElement('div');
        messageElement.textContent = `You: ${message}`;
        chatDisplay.appendChild(messageElement);

        // Send the message to the backend for moderation
        try {
            request_params = {
                method: 'POST',
                body: JSON.stringify({ message }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }
            console.log(request_params);
            const response = await fetch('https://movvgsbtq5.execute-api.eu-west-1.amazonaws.com/prod/moderation', request_params);
            if (response.ok) {
                const result = await response.json();
                // Update moderation checks
                updateModerationChecks(result);
            } else {
                console.error('Error:', response.statusText);
            }

        } catch (error) {
            console.error('Error during moderation:', error);
        }
        messageInput.value = '';
    });

    function updateModerationChecks(result) {
        moderationChecks.cyberbullying.className = result.cyberbullying ? 'red' : 'green';
        moderationChecks.notAgeAppropriate.className = result.notAgeAppropriate ? 'red' : 'green';
        moderationChecks.personalInfo.className = result.personalInfo ? 'red' : 'green';
        moderationChecks.strangerDanger.className = result.strangerDanger ? 'red' : 'green';
        moderationChecks.languageFilter.className = result.languageFilter ? 'red' : 'green';
        moderationChecks.negativeCommunication.className = result.negativeCommunication ? 'red' : 'green';
    }
});