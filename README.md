# Discord Server Manager Bot

A comprehensive Discord bot for server management with moderation, leveling, welcome messages, and fun commands.

## Features

### 🛡️ Moderation
- **Kick** - Remove members from the server
- **Ban** - Ban members from the server
- **Warn** - Issue warnings (auto-kick after 3 warnings)
- **Mute** - Temporarily or permanently mute members
- **Unmute** - Remove mute from members
- **Purge** - Delete messages in bulk

### 📊 Leveling System
- **Level** - Check user levels and progress
- **Leaderboard** - View top 10 members by level
- **AddXP** - Manually add XP to users (Admin)
- **ResetXP** - Reset user progression (Admin)

### 👋 Welcome & Goodbye
- **SetWelcome** - Configure welcome messages
- **SetGoodbye** - Configure goodbye messages
- **TestWelcome** - Test welcome message
- **TestGoodbye** - Test goodbye message
- Custom message variables and templates

### 🎮 Fun Commands
- **8Ball** - Ask the magic 8 ball
- **CoinFlip** - Flip a coin
- **Roll** - Roll a dice
- **Joke** - Get a random joke
- **RPS** - Play rock paper scissors

### ℹ️ Utility & Information
- **Ping** - Check bot latency
- **BotInfo** - Get bot information
- **ServerInfo** - Get server details
- **UserInfo** - Get user information
- **Avatar** - View user avatar
- **Stats** - View bot statistics
- **Invite** - Get bot invite link
- **Help** - Show available commands

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Discord Bot Token
- MongoDB (optional, for database features)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/chavdakanubhai2377/discord-server-manager-bot.git
   cd discord-server-manager-bot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your Discord token and settings
   ```

5. **Run the bot**
   ```bash
   python main.py
   ```

## Configuration

### Environment Variables (.env)
```env
DISCORD_TOKEN=your_bot_token_here
BOT_PREFIX=!
MONGODB_URI=mongodb://localhost:27017/discord_bot
```

### Getting a Discord Bot Token
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Go to "Bot" section and click "Add Bot"
4. Copy the token under USERNAME
5. Enable these Intents:
   - Message Content Intent
   - Server Members Intent
   - Moderation Intent

## Usage

### Common Commands

**Moderation:**
```
!kick @user [reason] - Kick a member
!ban @user [reason] - Ban a member
!warn @user [reason] - Warn a member
!mute @user [time] [reason] - Mute a member
!unmute @user - Unmute a member
!purge [amount] - Delete messages
```

**Leveling:**
```
!level [@user] - Check level
!leaderboard - View top members
!addxp @user <amount> - Add XP (Admin)
!resetxp @user - Reset XP (Admin)
```

**Welcome System:**
```
!setwelcome [channel] [message] - Set welcome message
!setgoodbye [channel] [message] - Set goodbye message
!testwelcome - Test welcome message
!testgoodbye - Test goodbye message
```

**Message Variables:**
- `{user}` - User mention
- `{username}` - Username
- `{server}` - Server name
- `{count}` - Member count

**Fun:**
```
!8ball <question> - Ask magic 8 ball
!coinflip - Flip a coin
!roll [sides] - Roll a dice
!joke - Get a joke
!rps <rock|paper|scissors> - Play RPS
```

**Utility:**
```
!ping - Check latency
!botinfo - Bot information
!serverinfo - Server information
!userinfo [@user] - User information
!avatar [@user] - View avatar
!stats - Bot statistics
!invite - Get invite link
!help - Show all commands
```

## Keeping Bot 24/7 Online

### Option 1: Hosting Services (Recommended)

#### **Replit**
1. Fork the repository to Replit
2. Set environment variables in Secrets
3. Install UptimeRobot (free) to ping the bot every 5 minutes
4. Cost: Free

#### **Heroku** (formerly free, now paid)
1. Create Heroku account
2. Deploy using Git
3. Add Procfile with: `worker: python main.py`
4. Cost: ~$7/month minimum

#### **PythonAnywhere**
1. Create account at PythonAnywhere.com
2. Upload files via web interface
3. Create scheduled task to run bot
4. Cost: Free tier available

#### **Glitch**
1. Import GitHub repo to Glitch
2. Set up environment variables
3. Enable project to stay awake
4. Cost: Free

### Option 2: VPS Hosting

#### **DigitalOcean**
1. Create Droplet (Ubuntu 20.04)
2. SSH into server: `ssh root@your_ip`
3. Install Python: `sudo apt-get install python3 python3-pip`
4. Clone repository and install dependencies
5. Use systemd service (see below)
6. Cost: $5-6/month

#### **AWS EC2**
1. Launch free tier instance
2. SSH into instance
3. Install Python and dependencies
4. Set up systemd service
5. Cost: Free tier available

### Option 3: Systemd Service (Linux/VPS)

Create `/etc/systemd/system/discord-bot.service`:
```ini
[Unit]
Description=Discord Server Manager Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/discord-server-manager-bot
Environment="PATH=/path/to/discord-server-manager-bot/venv/bin"
ExecStart=/path/to/discord-server-manager-bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable discord-bot
sudo systemctl start discord-bot
sudo systemctl status discord-bot
```

### Option 4: Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "main.py"]
```

Build and run:
```bash
docker build -t discord-bot .
docker run -d --name discord-bot -e DISCORD_TOKEN=your_token discord-bot
```

### Option 5: GitHub Actions (Free)

Create `.github/workflows/bot.yml`:
```yaml
name: Run Discord Bot

on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: python main.py
        env:
          DISCORD_TOKEN: ${{ secrets.DISCORD_TOKEN }}
```

## Recommended Setup for 24/7

**Best Option: DigitalOcean + Systemd**
- Cost: $5/month
- Reliability: 99.9% uptime
- Setup time: 15-20 minutes
- Easy to manage and scale

## Database Setup (Optional)

### MongoDB Atlas (Cloud)
1. Create free account at mongodb.com/cloud/atlas
2. Create cluster
3. Get connection string
4. Add to `.env`: `MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/database`

### Local MongoDB
```bash
# Install MongoDB
sudo apt-get install mongodb

# Start MongoDB
sudo service mongod start

# Connection string
MONGODB_URI=mongodb://localhost:27017/discord_bot
```

## Troubleshooting

### Bot Won't Start
- Check Discord token in `.env`
- Verify Python 3.8+ installed
- Install all dependencies: `pip install -r requirements.txt`
- Check logs: `python main.py`

### Commands Not Working
- Verify bot has permissions in channel
- Check prefix in `.env` (default: `!`)
- Ensure intents enabled in Developer Portal
- Bot needs "Administrator" permission

### Bot Disconnects
- Check internet connection
- Verify token is still valid
- Check rate limiting
- Use restart service (systemd/Docker handles this)

### High Memory Usage
- Check for memory leaks in cogs
- Limit number of concurrent processes
- Use proper cleanup in event listeners

## Project Structure

```
discord-server-manager-bot/
├── main.py              # Bot entry point
├── config.py            # Configuration
├── requirements.txt     # Dependencies
├── .env.example         # Environment template
├── .gitignore          # Git ignore rules
├── cogs/               # Command modules
│   ├── moderation.py   # Moderation commands
│   ├── leveling.py     # Leveling system
│   ├── welcome.py      # Welcome/goodbye
│   ├── utility.py      # Info commands
│   └── fun.py          # Fun commands
└── README.md           # This file
```

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and commit: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues or questions:
1. Check GitHub Issues
2. Review Troubleshooting section
3. Contact: chavdakanubhai2377@gmail.com

## Resources

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/)
- [Discord.py GitHub](https://github.com/Rapptz/discord.py)
- [Python Documentation](https://docs.python.org/3/)

## Roadmap

- [ ] Music player integration
- [ ] Custom commands system
- [ ] Reaction roles
- [ ] Ticket system
- [ ] Auto-moderation
- [ ] Statistics dashboard
- [ ] Web dashboard
- [ ] Multi-language support

---

**Made with ❤️ by chavdakanubhai2377**

Last Updated: 2026-08-27
