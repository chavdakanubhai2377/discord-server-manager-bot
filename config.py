import os
from dotenv import load_dotenv

load_dotenv()

# Discord Bot Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
BOT_PREFIX = os.getenv('BOT_PREFIX', '!')
BOT_INTENTS = {
    'message_content': True,
    'members': True,
    'moderation': True,
    'guilds': True,
    'guild_messages': True,
    'direct_messages': True,
}

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/discord_bot')
MONGODB_USER = os.getenv('MONGODB_USER')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')

# Database Collections
COLLECTIONS = {
    'users': 'users',
    'guilds': 'guilds',
    'moderation': 'moderation_logs',
    'music': 'music_settings',
    'roles': 'role_configs',
    'welcomes': 'welcome_messages',
}

# Feature Flags
FEATURES = {
    'moderation': True,
    'leveling': True,
    'music': True,
    'automod': True,
    'welcome': True,
    'logging': True,
}

# Moderation Settings
MODERATION = {
    'max_warnings': 3,
    'cooldown_per_violation': 300,  # 5 minutes
}
