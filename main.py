import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Get bot token and prefix from environment
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('BOT_PREFIX', '!')

# Create bot instance with intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.moderation = True
intents.reactions = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Bot info
BOT_NAME = os.getenv('BOT_NAME', 'TableMC Development')
BOT_VERSION = os.getenv('BOT_VERSION', '1.0.0')

@bot.event
async def on_ready():
    """Called when the bot is ready"""
    print(f"\n{'='*50}")
    print(f"✅ {BOT_NAME} is now online!")
    print(f"{'='*50}")
    print(f"🤖 Bot Name: {bot.user.name}")
    print(f"🆔 Bot ID: {bot.user.id}")
    print(f"📌 Prefix: {PREFIX}")
    print(f"📊 Servers: {len(bot.guilds)}")
    print(f"👥 Users: {sum(g.member_count for g in bot.guilds)}")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")
    
    # Set bot status
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name=f"{PREFIX}help | TableMC Development"
    )
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.event
async def on_guild_join(guild):
    """Called when bot joins a new guild"""
    print(f"✅ Joined new server: {guild.name} (ID: {guild.id})")
    print(f"   Members: {guild.member_count}")

@bot.event
async def on_guild_remove(guild):
    """Called when bot leaves a guild"""
    print(f"❌ Left server: {guild.name} (ID: {guild.id})")

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="❌ Permission Denied",
            description="You don't have permission to use this command!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="❌ Missing Arguments",
            description=f"Missing required argument: `{error.param.name}`",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandNotFound):
        pass  # Silently ignore unknown commands
    else:
        print(f"⚠️ Error: {error}")

@bot.command(name='ping')
async def ping(ctx):
    """Check bot latency"""
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Bot latency: `{round(bot.latency * 1000)}ms`",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

@bot.command(name='status')
async def status(ctx):
    """Get bot status information"""
    embed = discord.Embed(
        title="📊 Bot Status",
        color=discord.Color.blue()
    )
    embed.add_field(name="🤖 Name", value=BOT_NAME, inline=True)
    embed.add_field(name="📌 Version", value=BOT_VERSION, inline=True)
    embed.add_field(name="🆔 Bot ID", value=f"`{bot.user.id}`", inline=True)
    embed.add_field(name="📡 Latency", value=f"`{round(bot.latency * 1000)}ms`", inline=True)
    embed.add_field(name="🌍 Servers", value=f"`{len(bot.guilds)}`", inline=True)
    embed.add_field(name="👥 Total Users", value=f"`{sum(g.member_count for g in bot.guilds)}`", inline=True)
    embed.add_field(name="⏰ Uptime", value=f"Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", inline=False)
    embed.add_field(name="✅ Cogs Loaded", value=f"`{len(bot.cogs)}` cogs active", inline=True)
    embed.set_footer(text=f"TableMC Development • {BOT_VERSION}", icon_url=bot.user.avatar.url)
    
    await ctx.send(embed=embed)

@bot.command(name='help')
async def help_command(ctx):
    """Show help information"""
    embed = discord.Embed(
        title="📚 Help - Available Commands",
        description=f"Use `{PREFIX}command_name` to execute commands",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="🔐 Moderation",
        value=f"`{PREFIX}kick`, `{PREFIX}ban`, `{PREFIX}warn`, `{PREFIX}mute`, `{PREFIX}unmute`, `{PREFIX}purge`",
        inline=False
    )
    
    embed.add_field(
        name="👋 Welcome System",
        value=f"`{PREFIX}welcome` - Full welcome system configuration",
        inline=False
    )
    
    embed.add_field(
        name="🎫 Ticket System",
        value=f"`{PREFIX}ticket` - Setup and manage support tickets",
        inline=False
    )
    
    embed.add_field(
        name="🤖 Auto-Responder",
        value=f"`{PREFIX}autoresponse` - Setup automatic keyword responses",
        inline=False
    )
    
    embed.add_field(
        name="🎭 Reaction Roles",
        value=f"`{PREFIX}reactionrole` - Setup self-assignable roles",
        inline=False
    )
    
    embed.add_field(
        name="ℹ️ Information",
        value=f"`{PREFIX}ping`, `{PREFIX}status`, `{PREFIX}help`",
        inline=False
    )
    
    embed.set_footer(text=f"TableMC Development • {BOT_VERSION}")
    
    await ctx.send(embed=embed)

async def load_cogs():
    """Load all cogs from the cogs directory"""
    cogs_dir = "cogs"
    
    if not os.path.exists(cogs_dir):
        print(f"⚠️ Warning: {cogs_dir} directory not found!")
        return
    
    cog_count = 0
    for filename in os.listdir(cogs_dir):
        if filename.endswith('.py') and not filename.startswith('_'):
            cog_name = filename[:-3]
            try:
                await bot.load_extension(f'{cogs_dir}.{cog_name}')
                print(f"✅ Loaded cog: {cog_name}")
                cog_count += 1
            except Exception as e:
                print(f"❌ Failed to load cog {cog_name}: {e}")
    
    print(f"\n📦 Total cogs loaded: {cog_count}\n")

async def main():
    """Main function to start the bot"""
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

if __name__ == "__main__":
    if not TOKEN:
        print("❌ Error: DISCORD_TOKEN not found in .env file!")
        print("Please set your Discord bot token in the .env file")
        exit(1)
    
    print(f"\n🚀 Starting {BOT_NAME} v{BOT_VERSION}...")
    print(f"📌 Prefix: {PREFIX}")
    print(f"{'='*50}\n")
    
    import asyncio
    asyncio.run(main())
