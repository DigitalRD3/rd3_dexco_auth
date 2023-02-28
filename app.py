import app_config
import os

from flask import Flask, request
import msal

app = Flask(__name__)

# Define the MSAL client application parameters
client_id = os.getenv('CLIENT_ID')
authority = os.getenv('AUTHORITY')
client_secret = os.getenv('CLIENT_SECRET')
scope = app_config.SCOPE

# Create a new MSAL application instance with the client_id and authority parameters
app_client = msal.ConfidentialClientApplication(
    client_id=client_id,
    authority=authority,
    client_credential=client_secret
)

# Define the route for the authentication endpoint
@app.route('/authenticate', methods=['POST'])
def authenticate():
    # Get the username and password from the POST request JSON body
    data = request.get_json()
    username = data['username']
    password = data['pw']
    
    # Authenticate the user with MSAL and retrieve an access token
    result = app_client.acquire_token_by_username_password(
        username=username,
        password=password,
        scopes=scope
    )
    
    # Return the access token in the response
    if 'access_token' in result:
        access_token = result['access_token']
        print('Success')
        print(result[access_token])
        return {'access_token': access_token}
    else:
        print('Error')
        return {'error': result.get('error')}

if __name__ == '__main__':
    app.run(debug=True)
