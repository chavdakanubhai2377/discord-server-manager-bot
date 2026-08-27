import discord
from discord.ext import commands
from datetime import datetime

class Welcome(commands.Cog):
    """Welcome and goodbye messages system"""
    
    def __init__(self, bot):
        self.bot = bot
        self.welcome_messages = {}  # {guild_id: {'channel_id': int, 'message': str}}
        self.goodbye_messages = {}  # {guild_id: {'channel_id': int, 'message': str}}
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Send welcome message when member joins"""
        guild_id = member.guild.id
        
        if guild_id not in self.welcome_messages:
            return
        
        config = self.welcome_messages[guild_id]
        channel = member.guild.get_channel(config['channel_id'])
        
        if not channel:
            return
        
        # Parse message with user info
        message = config['message'].format(
            user=member.mention,
            username=member.name,
            server=member.guild.name,
            count=member.guild.member_count
        )
        
        embed = discord.Embed(
            title=f'👋 Welcome {member.name}!',
            description=message,
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        embed.add_field(name='Member Count', value=f'You are member #{member.guild.member_count}')
        embed.set_footer(text=f'Joined at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        
        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            pass
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Send goodbye message when member leaves"""
        guild_id = member.guild.id
        
        if guild_id not in self.goodbye_messages:
            return
        
        config = self.goodbye_messages[guild_id]
        channel = member.guild.get_channel(config['channel_id'])
        
        if not channel:
            return
        
        # Parse message with user info
        message = config['message'].format(
            user=member.mention,
            username=member.name,
            server=member.guild.name
        )
        
        embed = discord.Embed(
            title=f'👋 Goodbye {member.name}',
            description=message,
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        embed.set_footer(text=f'Left at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        
        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            pass
    
    @commands.command(name='setwelcome', help='Set welcome message')
    @commands.has_permissions(administrator=True)
    async def setwelcome(self, ctx, channel: discord.TextChannel = None, *, message: str = None):
        """Set welcome message for new members"""
        if channel is None:
            channel = ctx.channel
        
        if message is None:
            message = 'Welcome {user} to {server}! We now have {count} members!'
        
        guild_id = ctx.guild.id
        self.welcome_messages[guild_id] = {
            'channel_id': channel.id,
            'message': message
        }
        
        embed = discord.Embed(
            title='✓ Welcome Message Set',
            description=f'Channel: {channel.mention}',
            color=discord.Color.green()
        )
        embed.add_field(name='Message', value=f'```{message}```', inline=False)
        embed.add_field(name='Variables', value='`{user}` - User mention\n`{username}` - Username\n`{server}` - Server name\n`{count}` - Member count', inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='setgoodbye', help='Set goodbye message')
    @commands.has_permissions(administrator=True)
    async def setgoodbye(self, ctx, channel: discord.TextChannel = None, *, message: str = None):
        """Set goodbye message for leaving members"""
        if channel is None:
            channel = ctx.channel
        
        if message is None:
            message = 'Goodbye {user}! We\'re sad to see you leave {server}!'
        
        guild_id = ctx.guild.id
        self.goodbye_messages[guild_id] = {
            'channel_id': channel.id,
            'message': message
        }
        
        embed = discord.Embed(
            title='✓ Goodbye Message Set',
            description=f'Channel: {channel.mention}',
            color=discord.Color.green()
        )
        embed.add_field(name='Message', value=f'```{message}```', inline=False)
        embed.add_field(name='Variables', value='`{user}` - User mention\n`{username}` - Username\n`{server}` - Server name', inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='testwelcome', help='Test welcome message')
    @commands.has_permissions(administrator=True)
    async def testwelcome(self, ctx):
        """Test the welcome message"""
        guild_id = ctx.guild.id
        
        if guild_id not in self.welcome_messages:
            await ctx.send('❌ No welcome message configured!')
            return
        
        config = self.welcome_messages[guild_id]
        channel = ctx.guild.get_channel(config['channel_id'])
        
        if not channel:
            await ctx.send('❌ Welcome channel not found!')
            return
        
        message = config['message'].format(
            user=ctx.author.mention,
            username=ctx.author.name,
            server=ctx.guild.name,
            count=ctx.guild.member_count
        )
        
        embed = discord.Embed(
            title=f'👋 Welcome {ctx.author.name}! (TEST)',
            description=message,
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed.add_field(name='Member Count', value=f'You are member #{ctx.guild.member_count}')
        embed.set_footer(text='This is a test message')
        
        await channel.send(embed=embed)
        await ctx.send('✓ Test message sent!')
    
    @commands.command(name='testgoodbye', help='Test goodbye message')
    @commands.has_permissions(administrator=True)
    async def testgoodbye(self, ctx):
        """Test the goodbye message"""
        guild_id = ctx.guild.id
        
        if guild_id not in self.goodbye_messages:
            await ctx.send('❌ No goodbye message configured!')
            return
        
        config = self.goodbye_messages[guild_id]
        channel = ctx.guild.get_channel(config['channel_id'])
        
        if not channel:
            await ctx.send('❌ Goodbye channel not found!')
            return
        
        message = config['message'].format(
            user=ctx.author.mention,
            username=ctx.author.name,
            server=ctx.guild.name
        )
        
        embed = discord.Embed(
            title=f'👋 Goodbye {ctx.author.name}! (TEST)',
            description=message,
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed.set_footer(text='This is a test message')
        
        await channel.send(embed=embed)
        await ctx.send('✓ Test message sent!')

async def setup(bot):
    await bot.add_cog(Welcome(bot))
