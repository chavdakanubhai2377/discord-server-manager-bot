import discord
from discord.ext import commands
from datetime import datetime

class PremiumWelcomer(commands.Cog):
    """Premium welcome and goodbye messages with custom embeds"""
    
    def __init__(self, bot):
        self.bot = bot
        self.welcome_settings = {}  # {guild_id: {channel_id, message, enabled}}
        self.goodbye_settings = {}  # {guild_id: {channel_id, message, enabled}}
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Send welcome message when member joins"""
        if member.guild.id not in self.welcome_settings:
            return
        
        settings = self.welcome_settings[member.guild.id]
        if not settings.get('enabled', True):
            return
        
        channel = self.bot.get_channel(settings['channel_id'])
        if not channel:
            return
        
        message_template = settings.get('message', '')
        
        # Replace variables
        message = message_template.format(
            user=member.mention,
            username=member.name,
            server=member.guild.name,
            count=member.guild.member_count,
            tag=member.discriminator
        )
        
        # Create premium embed
        embed = discord.Embed(
            title="✨ Welcome to TableMC Development!",
            description=message,
            color=discord.Color.from_rgb(88, 165, 252)
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        embed.add_field(name="👤 Member", value=f"{member.mention}", inline=True)
        embed.add_field(name="🆔 User ID", value=f"`{member.id}`", inline=True)
        embed.add_field(name="📅 Account Created", value=member.created_at.strftime('%Y-%m-%d'), inline=False)
        embed.add_field(name="👥 Server Members", value=f"`{member.guild.member_count}`", inline=True)
        embed.set_footer(text=f"Welcome • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                        icon_url=member.guild.icon.url if member.guild.icon else None)
        
        try:
            await channel.send(f"{member.mention}", embed=embed)
        except discord.Forbidden:
            pass
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Send goodbye message when member leaves"""
        if member.guild.id not in self.goodbye_settings:
            return
        
        settings = self.goodbye_settings[member.guild.id]
        if not settings.get('enabled', True):
            return
        
        channel = self.bot.get_channel(settings['channel_id'])
        if not channel:
            return
        
        message_template = settings.get('message', '')
        
        # Replace variables
        message = message_template.format(
            user=member.mention,
            username=member.name,
            server=member.guild.name,
            count=member.guild.member_count,
            tag=member.discriminator
        )
        
        # Create premium goodbye embed
        embed = discord.Embed(
            title="👋 Goodbye!",
            description=message,
            color=discord.Color.from_rgb(240, 71, 71)
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        embed.add_field(name="👤 Member", value=f"{member.name}#{member.discriminator}", inline=True)
        embed.add_field(name="⏱️ Time in Server", value=f"`{(datetime.now() - member.joined_at).days} days`", inline=True)
        embed.add_field(name="👥 Members Left", value=f"`{member.guild.member_count}`", inline=True)
        embed.set_footer(text=f"Goodbye • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                        icon_url=member.guild.icon.url if member.guild.icon else None)
        
        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            pass
    
    @commands.command(name='setwelcome')
    @commands.has_permissions(manage_guild=True)
    async def setwelcome(self, ctx, channel: discord.TextChannel, *, message="Welcome {user} to {server}!"):
        """Set welcome message and channel"""
        self.welcome_settings[ctx.guild.id] = {
            'channel_id': channel.id,
            'message': message,
            'enabled': True
        }
        
        embed = discord.Embed(
            title="✨ Welcome Message Set",
            color=discord.Color.green()
        )
        embed.add_field(name="Channel", value=channel.mention, inline=False)
        embed.add_field(name="Message", value=f"```{message}```", inline=False)
        embed.add_field(name="Variables", value="`{user}` `{username}` `{server}` `{count}` `{tag}`", inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='setgoodbye')
    @commands.has_permissions(manage_guild=True)
    async def setgoodbye(self, ctx, channel: discord.TextChannel, *, message="Goodbye {user}! Thanks for visiting {server}"):
        """Set goodbye message and channel"""
        self.goodbye_settings[ctx.guild.id] = {
            'channel_id': channel.id,
            'message': message,
            'enabled': True
        }
        
        embed = discord.Embed(
            title="👋 Goodbye Message Set",
            color=discord.Color.green()
        )
        embed.add_field(name="Channel", value=channel.mention, inline=False)
        embed.add_field(name="Message", value=f"```{message}```", inline=False)
        embed.add_field(name="Variables", value="`{user}` `{username}` `{server}` `{count}` `{tag}`", inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='testwelcome')
    @commands.has_permissions(manage_guild=True)
    async def testwelcome(self, ctx):
        """Test welcome message"""
        if ctx.guild.id not in self.welcome_settings:
            await ctx.send("❌ No welcome message configured! Use `!setwelcome` first.")
            return
        
        settings = self.welcome_settings[ctx.guild.id]
        channel = self.bot.get_channel(settings['channel_id'])
        
        if not channel:
            await ctx.send("❌ Welcome channel not found!")
            return
        
        message = settings['message'].format(
            user=ctx.author.mention,
            username=ctx.author.name,
            server=ctx.guild.name,
            count=ctx.guild.member_count,
            tag=ctx.author.discriminator
        )
        
        embed = discord.Embed(
            title="✨ Welcome to TableMC Development!",
            description=message,
            color=discord.Color.from_rgb(88, 165, 252)
        )
        embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed.add_field(name="👤 Member", value=f"{ctx.author.mention}", inline=True)
        embed.add_field(name="🆔 User ID", value=f"`{ctx.author.id}`", inline=True)
        embed.add_field(name="📅 Account Created", value=ctx.author.created_at.strftime('%Y-%m-%d'), inline=False)
        embed.add_field(name="👥 Server Members", value=f"`{ctx.guild.member_count}`", inline=True)
        embed.set_footer(text=f"Welcome • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                        icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
        
        try:
            await channel.send(f"{ctx.author.mention}", embed=embed)
            await ctx.send("✅ Test welcome message sent!")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to send messages in that channel!")
    
    @commands.command(name='testgoodbye')
    @commands.has_permissions(manage_guild=True)
    async def testgoodbye(self, ctx):
        """Test goodbye message"""
        if ctx.guild.id not in self.goodbye_settings:
            await ctx.send("❌ No goodbye message configured! Use `!setgoodbye` first.")
            return
        
        settings = self.goodbye_settings[ctx.guild.id]
        channel = self.bot.get_channel(settings['channel_id'])
        
        if not channel:
            await ctx.send("❌ Goodbye channel not found!")
            return
        
        message = settings['message'].format(
            user=ctx.author.mention,
            username=ctx.author.name,
            server=ctx.guild.name,
            count=ctx.guild.member_count,
            tag=ctx.author.discriminator
        )
        
        embed = discord.Embed(
            title="👋 Goodbye!",
            description=message,
            color=discord.Color.from_rgb(240, 71, 71)
        )
        embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed.add_field(name="👤 Member", value=f"{ctx.author.name}#{ctx.author.discriminator}", inline=True)
        embed.add_field(name="⏱️ Time in Server", value=f"`{(datetime.now() - ctx.author.joined_at).days} days`", inline=True)
        embed.add_field(name="👥 Members Left", value=f"`{ctx.guild.member_count}`", inline=True)
        embed.set_footer(text=f"Goodbye • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                        icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
        
        try:
            await channel.send(embed=embed)
            await ctx.send("✅ Test goodbye message sent!")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to send messages in that channel!")
    
    @commands.command(name='welcomeoff')
    @commands.has_permissions(manage_guild=True)
    async def welcomeoff(self, ctx):
        """Disable welcome messages"""
        if ctx.guild.id in self.welcome_settings:
            self.welcome_settings[ctx.guild.id]['enabled'] = False
            await ctx.send("✅ Welcome messages disabled!")
        else:
            await ctx.send("❌ No welcome message configured!")
    
    @commands.command(name='welcomeon')
    @commands.has_permissions(manage_guild=True)
    async def welcomeon(self, ctx):
        """Enable welcome messages"""
        if ctx.guild.id in self.welcome_settings:
            self.welcome_settings[ctx.guild.id]['enabled'] = True
            await ctx.send("✅ Welcome messages enabled!")
        else:
            await ctx.send("❌ No welcome message configured!")

async def setup(bot):
    await bot.add_cog(PremiumWelcomer(bot))
