document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatDisplay = document.getElementById('chat-display');
    const spinner = document.getElementById('loading-spinner');

    const moderationChecks = {
        cyberbullying: document.getElementById('cyberbullying'),
        notAgeAppropriate: document.getElementById('age-appropriate'),
        personalInfo: document.getElementById('personal-info'),
        strangerDanger: document.getElementById('stranger-danger'),
        languageFilter: document.getElementById('language-filter'),
        negativeCommunication: document.getElementById('positive-communication')
    };

    function checkAcceptMessage(result){
        if(result.cyberbullying || result.notAgeAppropriate || result.personalInfo || result.strangerDanger || result.languageFilter || result.negativeCommunication){
            return false;
        }
        return true;
    }

    var elems = document.querySelectorAll('.tooltipped');
    var instances = M.Tooltip.init(elems);

    if (!form || !messageInput || !chatDisplay) {
        console.error('Required elements are missing in the DOM');
        return;
    }

    form.addEventListener('submit', async function(event) {
        event.preventDefault();

        const message = messageInput.value.trim();
        messageInput.value = '';

        if (message === '') return;

         // Show the spinner
         spinner.style.display = 'block';

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

                const messageElement = document.createElement('div');
                messageElement.style.padding = '10px';
                messageElement.style.borderRadius = '10px';
                messageElement.style.margin = '5px 0';
                messageElement.style.color = 'white'; // Optional: to make the text readable                
                
                if (checkAcceptMessage(result)){
                    // Display the message in the chat display with green color
                    messageElement.textContent = `You: ${message}`;
                    messageElement.style.backgroundColor = 'green';

                } else {
                    messageElement.textContent = `MESSAGE BLOCKED: ${message}`;
                    messageElement.style.backgroundColor = 'red';
                }
                chatDisplay.appendChild(messageElement);

            } else {
                console.error('Error:', response.statusText);
            }

        } catch (error) {
            console.error('Error during moderation:', error);
        } finally {
            // Hide the spinner
            spinner.style.display = 'none';
        }
        
    });

    function updateClass(element, condition) {
        if (condition) {
            element.classList.remove('green');
            element.classList.add('red');
        } else {
            element.classList.remove('red');
            element.classList.add('green');
        }
    }


    function updateModerationChecks(result) {
        updateClass(moderationChecks.cyberbullying, result.cyberbullying);
        updateClass(moderationChecks.notAgeAppropriate, result.notAgeAppropriate);
        updateClass(moderationChecks.personalInfo, result.personalInfo);
        updateClass(moderationChecks.strangerDanger, result.strangerDanger);
        updateClass(moderationChecks.languageFilter, result.languageFilter);
        updateClass(moderationChecks.negativeCommunication, result.negativeCommunication);
    }
});