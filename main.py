import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Bot configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
BOT_PREFIX = os.getenv('BOT_PREFIX', '!')

# Create bot instance
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.moderation = True

bot = commands.Bot(
    command_prefix=BOT_PREFIX,
    intents=intents,
    help_command=None,
    activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="TableMC Development"
    ),
    status=discord.Status.online
)

# Bot events
@bot.event
async def on_ready():
    """Called when bot successfully connects to Discord"""
    print(f'\n{"="*50}')
    print(f'Bot Name: TableMC Development')
    print(f'Logged in as: {bot.user}')
    print(f'Bot ID: {bot.user.id}')
    print(f'Prefix: {BOT_PREFIX}')
    print(f'Guilds: {len(bot.guilds)}')
    print(f'Users: {sum(len(guild.members) for guild in bot.guilds)}')
    print(f'Discord.py Version: {discord.__version__}')
    print(f'{"="*50}\n')

@bot.event
async def on_connect():
    """Called when bot connects to Discord (before ready)"""
    print(f'[TableMC Development] Connecting to Discord...')

@bot.event
async def on_disconnect():
    """Called when bot disconnects from Discord"""
    print(f'[TableMC Development] Disconnected from Discord')

@bot.event
async def on_resumed():
    """Called when bot resumes connection"""
    print(f'[TableMC Development] Connection resumed')

@bot.event
async def on_error(event, *args, **kwargs):
    """Handle errors"""
    print(f'[TableMC Development] Error in {event}:')
    import traceback
    traceback.print_exc()

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'❌ Command not found! Use `{BOT_PREFIX}help` for available commands.')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('❌ You do not have permission to use this command!')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'❌ Missing required argument: {error.param}')
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f'❌ Invalid argument provided: {error}')
    else:
        await ctx.send(f'❌ An error occurred: {error}')
        print(f'[TableMC Development] Error: {error}')

# Load cogs
async def load_cogs():
    """Load all cogs from the cogs directory"""
    cogs_dir = 'cogs'
    
    if not os.path.exists(cogs_dir):
        print(f'[TableMC Development] Cogs directory not found!')
        return
    
    for filename in os.listdir(cogs_dir):
        if filename.endswith('.py') and not filename.startswith('_'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'[TableMC Development] ✓ Loaded cog: {filename[:-3]}')
            except Exception as e:
                print(f'[TableMC Development] ✗ Failed to load cog {filename[:-3]}: {e}')

async def main():
    """Start the bot"""
    async with bot:
        await load_cogs()
        try:
            print(f'[TableMC Development] Starting bot...')
            await bot.start(DISCORD_TOKEN)
        except discord.errors.LoginFailure:
            print(f'[TableMC Development] ✗ Login failed! Check your Discord token.')
        except Exception as e:
            print(f'[TableMC Development] ✗ Failed to start bot: {e}')

# Run the bot
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f'\n[TableMC Development] Bot shutting down...')
    except Exception as e:
        print(f'[TableMC Development] Unexpected error: {e}')
