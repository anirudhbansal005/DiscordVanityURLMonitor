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

# Headers for authorization
BOT_TOKEN = "BOT_TOKEN" # Bot token won't work. So, use an alternate account's token
headers = {
    'Authorization': f'{BOT_TOKEN}', 
    'Content-Type': 'application/json',
}

def is_vanity_url_available():
    global invalid_request_counter
    try:
        response = requests.head(VANITY_CHECK_URL, allow_redirects=False)
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
    data = {"code": DESIRED_VANITY_URL}
    response = requests.patch(TARGET_API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        print(f"Successfully claimed the vanity URL: {DESIRED_VANITY_URL}")
        return True
    elif response.status_code == 403:
        print("Bot doesn't have permission to change the vanity URL.")
    elif response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 1))
        print(f"Rate limited. Retrying after {retry_after} seconds...")
        time.sleep(retry_after)
    else:
        print(f"Failed to claim vanity URL. Status Code: {response.status_code} - {response.json().get('message')}")
    
    invalid_request_counter += 1
    print(f"Invalid request count: {invalid_request_counter}\nDiscord: cloudyork")
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
