const ApiUrl = "https://gqake4g4t6.execute-api.eu-west-1.amazonaws.com/prod/";

function joinPaths(...paths) {
    return paths
        .map((part, index) => {
            // Remove leading slashes from all but the first part
            if (index > 0) {
                part = part.replace(/^\/+/, '');
            }
            // Remove trailing slashes from all but the last part
            if (index < paths.length - 1) {
                part = part.replace(/\/+$/, '');
            }
            return part;
        })
        .join('/');
}


document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatDisplay = document.getElementById('chat-display');
    const spinner = document.getElementById('loading-spinner');
    const selector = document.getElementById('model-select');
    const moderationChecksDiv = document.getElementById('moderation-div');

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

        const selectedModel = selector.value;

        // Send the message to the backend for moderation
        try {

            const idToken = localStorage.getItem('idToken');
            if (!idToken) {
                throw new Error('User is not authenticated');
            }

            request_params = {
                method: 'POST',
                body: JSON.stringify({ 
                    message: message,
                    model_id: selectedModel
                }),
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': idToken
                }
            }
            console.log(request_params);

            const moderationApiUrl = joinPaths(ApiUrl, '/moderation');

            const response = await fetch(moderationApiUrl, request_params);
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
        moderationChecksDiv.style.display = 'flex';
        updateClass(moderationChecks.cyberbullying, result.cyberbullying);
        updateClass(moderationChecks.notAgeAppropriate, result.notAgeAppropriate);
        updateClass(moderationChecks.personalInfo, result.personalInfo);
        updateClass(moderationChecks.strangerDanger, result.strangerDanger);
        updateClass(moderationChecks.languageFilter, result.languageFilter);
        updateClass(moderationChecks.negativeCommunication, result.negativeCommunication);
    }
});