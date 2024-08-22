# How the Bot Works
This bot monitors a specified Discord vanity URL and automatically claims it for your server as soon as it becomes available. It performs the following tasks:

- **Monitoring:** The bot continuously checks the status of a desired vanity URL by sending HTTP requests.
- **Claiming:** Once the vanity URL becomes available (i.e., returns a 404 status), the bot attempts to claim it for the specified server.
- **Error Handling:** The bot handles rate limits by pausing and retrying, ensuring it doesn't exceed Discord's rate limits.
Features
- **Vanity URL Monitoring:** Tracks the availability of a specific vanity URL without being part of the server.
- **Invalid Request Counter:** Keeps track of failed attempts to claim the URL.

# How to Use
- **Set Up the Bot:**
Clone this repository to your local machine.
Install the required dependencies with `pip install -r requirements.txt.`
Replace the placeholders in the script with your bot token, server ID, and desired vanity URL.

- **Running the Bot:**
Run the bot using Python: `python3 main.py`
The bot will start monitoring the vanity URL and attempt to claim it as soon as it becomes available.

- **Monitor the Bot:**
The bot outputs logs to the console, showing its status and any actions taken.

- **Replace the following variables in the code with your own:**
BOT_TOKEN: Your bot's token.
TARGET_GUILD_ID: The ID of the server where you want to claim the vanity URL.
DESIRED_VANITY_URL: The vanity URL you wish to monitor and claim.

# Important Notes
- Ensure your bot has the appropriate permissions to change the vanity URL in the target server.
- Since Discord has removed the ability for bots to change vanity URLs directly, this code may not function as intended in all cases. **Use this code at your own risk.**
- This bot is intended for educational purposes only. Make sure you comply with Discord's Terms of Service when using this bot.
