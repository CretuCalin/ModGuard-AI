const UserPoolIdValue = "eu-west-1_TBJgrnzXC";
const ClientIdValue = "706fc7hi7r73nlpiqmtlgfcgs9";


document.addEventListener('DOMContentLoaded', function() {

    const poolData = {
        UserPoolId: UserPoolIdValue, // Replace with your User Pool ID
        ClientId: ClientIdValue // Replace with your User Pool Client ID
    };
    const userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);

    document.getElementById('loginForm').addEventListener('submit', function(event) {
        event.preventDefault();

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        const authenticationData = {
            Username: username,
            Password: password,
        };
        const authenticationDetails = new AmazonCognitoIdentity.AuthenticationDetails(authenticationData);

        const userData = {
            Username: username,
            Pool: userPool
        };
        const cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);

        cognitoUser.authenticateUser(authenticationDetails, {
            onSuccess: function(result) {
                idToken = result.getIdToken().getJwtToken();
                console.log('Login successful!');
                console.log('Access token: ' + idToken);
                // save to local storage
                localStorage.setItem('idToken', idToken);

                current_url = window.location.href
                window.location.href = current_url + "chat.html";
            },
            onFailure: function(err) {
                alert(err.message || JSON.stringify(err));
            }
        });
    });

});