# Discord Bot Features

## Server Monitoring
- **Uptime**: Tracks how long the server has been running.
- **Disk Usage**: Monitors total, used, and free disk space on the server.
- **CPU Usage**: Displays current CPU usage percentage.
- **GPU Usage**: Provides separate monitoring for NVIDIA and AMD (Radeon) GPUs, showing load and memory usage.
- **RAM Usage**: Displays total, used, and free RAM memory in GB.
- **Network Speed**: Measures download and upload speeds in Mbps.
- **IP Addresses**: Shows both internal and external IP addresses of the server.
- **Running Processes**: Lists the first five running processes on the server.

## Automatic Updates
The bot updates the server status message in the Discord channel every hour to ensure the information is always current.

## Running the Bot
1. **Create a new application on Discord**: Go to the [Discord Developer Portal](https://discord.com/developers/applications), create a new application, and add a bot to that application.
   
2. **Get your bot token**:
   - In the "Bot" tab of your application, copy your bot's token.

3. **Add the bot to your server**:
   - In the "OAuth2" tab of your application, select `bot`, check appropriate permissions, and use the generated URL to add the bot to your server.

4. **Modify and run the script**:
   - Replace `YOUR_DISCORD_BOT_TOKEN` in `discord_bot.py` with your actual bot token.
   - Replace `YOUR_CHANNEL_ID` in `discord_bot.py` with the ID of the channel where you want to display server status.
   - Run the bot script using Python:

     ```bash
     python discord_bot.py
     ```

5. **Use the `!status` command**:
   - In the Discord server where the bot is added, use `!status` command to see the current server status.

## Troubleshooting
- If you encounter any issues with the bot or the setup process, ensure all required Python libraries are correctly installed and that your bot token and channel ID are correctly configured.

## Contributing
Contributions are welcome! If you have any suggestions, improvements, or feature requests, feel free to create a pull request.
