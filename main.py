import requests
import time
from discord.ext import commands
from flask import Flask
import threading
# Flask web server setup
app = Flask(__name__)

@app.route('/')
def home():
    return f"Bot is running! Invalid request attempts: {invalid_request_counter}"

TARGET_GUILD_ID = "TARGET_GUILD_ID"
DESIRED_VANITY_URL = 'DESIRED_VANITY_URL'
TARGET_API_URL = f"https://discord.com/api/v10/guilds/{TARGET_GUILD_ID}/vanity-url"
VANITY_CHECK_URL = f"https://discord.com/api/v9/invites/{DESIRED_VANITY_URL}?with_counts=true&with_expiration=true"
invalid_request_counter = 0
session = requests.Session()
# Headers for authorization
BOT_TOKEN = "BOT_TOKEN" # Bot token won't work. So, use an alternate account's token
headers = {
    'Authorization': f'{BOT_TOKEN}', 
    'Content-Type': 'application/json',
}
data = {"code": DESIRED_VANITY_URL}

def is_vanity_url_available():
    global invalid_request_counter
    try:
        response = session.head(VANITY_CHECK_URL, headers=headers, allow_redirects=False)
        if response.status_code == 404:
            print(f"Vanity URL {DESIRED_VANITY_URL} is available!")
            return True
        elif response.status_code == 429:
            retry_after_raw = response.headers.get('Retry-After', '1')
            retry_after = int(retry_after_raw.split(',')[0])
            print(f"Rate limited. Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
        else:
            print(f"Vanity URL {DESIRED_VANITY_URL} is still taken. Status: {response.status_code}")
            invalid_request_counter += 1
            print(f"Invalid request count: {invalid_request_counter}")
            return False
    except requests.RequestException as e:
        print(f"Error checking vanity URL: {e}")
        return False

def claim_vanity_url():
    global invalid_request_counter #cloudyork's magic
    response = session.patch(TARGET_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        print(f"Successfully claimed the vanity URL: {DESIRED_VANITY_URL}")
        return True
    elif response.status_code == 403:
        print("Bot doesn't have permission to change the vanity URL.")
    elif response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 1))
        print(f"Rate limited. Retrying after {retry_after} seconds...")
        time.sleep(retry_after)
    elif response.status_code == 401:
        # MFA required
        result = response.json()
        if 'mfa' in result and 'ticket' in result['mfa']:
            mfa_ticket = result['mfa']['ticket']
            print("MFA required, handling 2FA...")
            complete_mfa(mfa_ticket)
    else:
        print(f"Failed to claim vanity URL. Status Code: {response.status_code} - {response.json().get('message')}")
    
    invalid_request_counter += 1
    print(f"Invalid request count: {invalid_request_counter}\nDiscord: cloudyork")
    return False

def complete_mfa(mfa_ticket): 
# Discord added MFA while updating the server's vanity URL.
# As of now, this code is likely not working, as Discord still forbids the request from proceeding.
    mfa_url = "https://discord.com/api/v9/mfa/finish"
    mfa_data = {
        "ticket": mfa_ticket,
        "mfa_type": "password",  # Adjust if using a different MFA type like TOTP
        "data": "your_account_password"  # Replace with actual password or TOTP
    }
    
    response = session.post(mfa_url, headers=headers, json=mfa_data)
    if response.status_code == 200:
        result = response.json()
        mfa_token = result.get('token')
        # Set the MFA token in headers
        session.headers.update({'X-Discord-MFA-Authorization': mfa_token})
        # Retry the original request to claim the vanity URL
        response = session.patch(TARGET_API_URL, json=data)
        claim_vanity_url()
    elif response.status_code == 429:
        retry_after = float(response.json().get("retry_after", 1))
        print(f"Rate limited during 2FA. Retrying after {retry_after} seconds...")
        time.sleep(retry_after)
    else:
        print(f"Failed to complete 2FA: {response.status_code} - {response.text}")
        return False
        
def run_monitor():
    while True:
        if is_vanity_url_available():
            success = claim_vanity_url()
            if success:
                break
        time.sleep(2)  # Wait 2 seconds before checking again
def run_web():
    app.run(host='0.0.0.0', port=8080)
if __name__ == "__main__":
    # Start the Flask app in a separate thread
    threading.Thread(target=run_web).start()
    
if __name__ == "__main__":
    run_monitor()
