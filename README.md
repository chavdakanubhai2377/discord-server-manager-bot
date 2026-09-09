# 🤖 TableMC Development - Discord Server Manager Bot

A premium, feature-rich Discord bot built with discord.py offering advanced server management, moderation, welcome systems, ticketing, auto-responses, and reaction roles.

## ✨ Features

### 🔐 Advanced Moderation
- **Kick & Ban System** - Remove problematic members with logging
- **Warning System** - Track member warnings (auto-kick at 3 warnings)
- **Mute System** - Temporary muting with auto-unmute
- **Message Purge** - Bulk delete messages from channels
- **Action Logging** - Comprehensive moderation action tracking

### 👋 Sapphire-Style Welcome System
- **Custom Welcome Messages** - Fully customizable welcome embeds
- **Member Information Display** - Shows account age, join position, etc.
- **Goodbye Messages** - Track member departures
- **Test Mode** - Preview messages before going live
- **Toggle Control** - Enable/disable welcomes per server

### 🎫 Premium Ticket System (Roti Bot Style)
- **Interactive Ticket Panel** - Button-based ticket creation
- **Auto-Categorization** - Tickets organized in dedicated category
- **Support Team Assignment** - Assign support roles
- **Ticket Transcripts** - Save conversation history
- **Quick Close** - React with 🔒 or use commands to close tickets

### 🤖 Auto-Responder
- **Keyword Triggers** - Automatic responses to specific keywords
- **Custom Responses** - Fully customizable reply messages
- **Search Function** - Find existing auto-responses
- **Edit & Manage** - Modify or delete responses as needed
- **Rich Embeds** - Beautiful formatted responses

### 🎭 Reaction Roles
- **Self-Assignable Roles** - Members get roles by reacting
- **Multiple Role Support** - Unlimited reaction-role pairs per message
- **Auto-Remove** - Roles removed when reaction is removed
- **Sync System** - Keep reactions in sync with configuration
- **Easy Management** - Simple commands to add/remove roles

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- discord.py 2.3.2+
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/chavdakanubhai2377/discord-server-manager-bot.git
cd discord-server-manager-bot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your Discord bot token
```

4. **Run the bot**
```bash
python main.py
```

## ⚙️ Configuration

### Environment Variables (.env)
```
DISCORD_TOKEN=your_bot_token_here
BOT_PREFIX=!
BOT_NAME=TableMC Development
```

Get your Discord bot token from [Discord Developer Portal](https://discord.com/developers/applications)

## 📚 Command Guide

### Moderation Commands
```
!kick <user> [reason]           - Kick a user
!ban <user> [reason]            - Ban a user
!warn <user> [reason]           - Warn a user
!mute <user> <minutes> [reason] - Mute a user
!unmute <user>                  - Unmute a user
!purge <amount>                 - Delete messages
```

### Welcome System
```
!welcome channel <#channel>              - Set welcome channel
!welcome title <text>                    - Set welcome title
!welcome description <text>              - Set description
!welcome image <url>                     - Set welcome image
!welcome test                            - Test welcome message
!welcome toggle                          - Toggle on/off
!welcome preview                         - View current settings
```

Variables: `{user}` `{username}` `{server}` `{count}` `{id}` `{tag}`

### Ticket System
```
!ticket setup <category> <role>    - Initialize tickets
!ticket create                     - Create a ticket
!ticket close                      - Close current ticket
!ticket panel                      - Send creation panel
!ticket status                     - Check ticket info
```

### Auto-Responder
```
!autoresponse add <trigger> <response>   - Add response
!autoresponse remove <trigger>           - Delete response
!autoresponse list                       - List all responses
!autoresponse edit <trigger> <response>  - Modify response
!autoresponse search <keyword>           - Search responses
!autoresponse clear                      - Delete all
```

### Reaction Roles
```
!reactionrole create <title>                    - Create message
!reactionrole add <msg_id> <emoji> <role>      - Add role pair
!reactionrole remove <msg_id> <emoji>          - Remove role pair
!reactionrole list [msg_id]                    - View roles
!reactionrole delete <msg_id>                  - Delete message
!reactionrole sync <msg_id>                    - Sync reactions
```

## 📁 Project Structure

```
discord-server-manager-bot/
├── main.py                    # Bot entry point
├── .env.example              # Environment template
├── requirements.txt          # Dependencies
├── README.md                 # This file
└── cogs/
    ├── advanced_moderation.py    # Moderation system
    ├── sapphire_welcome.py       # Welcome messages
    ├── premium_tickets.py        # Ticket system
    ├── auto_responder.py         # Auto-responses
    └── reaction_roles.py         # Reaction roles
```

## 🔐 Permissions

The bot requires the following permissions:
- Manage Messages
- Manage Members
- Manage Roles
- Manage Channels
- Send Messages
- Embed Links
- Add Reactions
- Read Message History

## 🎯 Use Cases

- **Server Moderation** - Comprehensive tools for server admins
- **Welcome Automation** - Professional member onboarding
- **Support Tickets** - Organized customer support
- **User Engagement** - Reaction roles for member roles
- **FAQ Automation** - Auto-respond to common questions

## 🐛 Troubleshooting

### Bot not responding
- Check bot token in .env
- Ensure bot has proper permissions
- Verify bot is online in Discord

### Commands not working
- Use correct prefix (default: `!`)
- Ensure you have required permissions
- Check bot role hierarchy for role commands

### Welcome messages not sending
- Configure channel with `!welcome channel`
- Ensure bot can send messages in channel
- Verify feature is enabled with `!welcome toggle`

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👨‍💻 Author

**Pratik Chavda**
- GitHub: [@chavdakanubhai2377](https://github.com/chavdakanubhai2377)
- Email: chavdakanubhai2377@gmail.com

## 🙏 Acknowledgments

- [discord.py](https://github.com/Rapptz/discord.py) - Discord API wrapper
- [Sapphire Bot](https://sapphirebot.com/) - Inspiration for welcome system
- [Roti Bot](https://rotiabot.com/) - Inspiration for ticket system

## 📞 Support

For issues and feature requests, please [create an issue](https://github.com/chavdakanubhai2377/discord-server-manager-bot/issues)

## 🔄 Updates

This bot is actively maintained. Updates include:
- Bug fixes
- New features
- Performance improvements
- Security patches

---

**Made with ❤️ by TableMC Development**

Last Updated: 2026-09-09
