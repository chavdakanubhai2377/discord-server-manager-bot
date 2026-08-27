import discord
from discord.ext import commands
import os
import sys
from config import DISCORD_TOKEN, BOT_PREFIX

# Setup bot intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.moderation = True

# Initialize bot
bot = commands.Bot(
    command_prefix=BOT_PREFIX,
    intents=intents,
    help_command=commands.DefaultHelpCommand()
)

# Load Cogs (Extensions)
async def load_cogs():
    cogs_dir = 'cogs'
    if not os.path.exists(cogs_dir):
        os.makedirs(cogs_dir)
    
    for filename in os.listdir(cogs_dir):
        if filename.endswith('.py') and not filename.startswith('_'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'✓ Loaded cog: {filename}')
            except Exception as e:
                print(f'✗ Failed to load cog {filename}: {e}')

@bot.event
async def on_ready():
    print(f'\n✓ Bot logged in as: {bot.user}')
    print(f'✓ Bot ID: {bot.user.id}')
    print(f'✓ Connected to {len(bot.guilds)} guild(s)')
    
    # Set bot activity
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f'{BOT_PREFIX}help | Managing {len(bot.guilds)} servers'
        )
    )

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'❌ Command not found. Use `{BOT_PREFIX}help` to see available commands.')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('❌ You don\'t have permission to use this command.')
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send('❌ I don\'t have permission to perform this action.')
    else:
        await ctx.send(f'❌ An error occurred: {error}')
        print(f'Error: {error}')

async def main():
    async with bot:
        # Load all cogs
        await load_cogs()
        
        # Start the bot
        try:
            await bot.start(DISCORD_TOKEN)
        except discord.LoginFailure:
            print('❌ Invalid Discord token. Please check your .env file.')
            sys.exit(1)

if __name__ == '__main__':
    print('🤖 Starting Discord Server Manager Bot...')
    
    try:
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\n✓ Bot shutdown gracefully')
