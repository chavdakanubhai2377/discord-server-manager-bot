import discord
from discord.ext import commands
from datetime import datetime

class SapphireWelcomer(commands.Cog):
    """Sapphire-style premium welcome system with interactive embeds"""
    
    def __init__(self, bot):
        self.bot = bot
        self.welcome_settings = {}  # {guild_id: {channel_id, title, description, color, image_url, enabled}}
        self.goodbye_settings = {}
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Send Sapphire-style welcome message"""
        if member.guild.id not in self.welcome_settings:
            return
        
        settings = self.welcome_settings[member.guild.id]
        if not settings.get('enabled', True):
            return
        
        channel = self.bot.get_channel(settings['channel_id'])
        if not channel:
            return
        
        # Replace variables
        def replace_vars(text):
            return text.format(
                user=member.mention,
                username=member.name,
                server=member.guild.name,
                count=member.guild.member_count,
                tag=member.discriminator,
                id=member.id
            )
        
        title = replace_vars(settings.get('title', 'Welcome to {server}!'))
        description = replace_vars(settings.get('description', 'Welcome {user}!'))
        
        # Create Sapphire-style embed
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.from_rgb(88, 165, 252)
        )
        
        # Add member info section
        embed.add_field(
            name="👤 Member Info",
            value=f"**Name:** {member.mention}\n**Tag:** {member.name}#{member.discriminator}\n**ID:** `{member.id}`",
            inline=False
        )
        
        # Add account info
        created_days = (datetime.now() - member.created_at).days
        embed.add_field(
            name="📅 Account Info",
            value=f"**Created:** {member.created_at.strftime('%B %d, %Y')}\n**Age:** {created_days} days old",
            inline=False
        )
        
        # Add server info
        embed.add_field(
            name="👥 Server Info",
            value=f"**Members:** {member.guild.member_count}\n**Joined as:** Member #{member.guild.member_count}",
            inline=False
        )
        
        # Set thumbnail and image
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        if settings.get('image_url'):
            embed.set_image(url=settings['image_url'])
        
        embed.set_footer(
            text=f"TableMC Development • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            icon_url=member.guild.icon.url if member.guild.icon else None
        )
        
        try:
            # Send with role mention
            await channel.send(f"Welcome {member.mention}!", embed=embed)
        except discord.Forbidden:
            pass
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Send Sapphire-style goodbye message"""
        if member.guild.id not in self.goodbye_settings:
            return
        
        settings = self.goodbye_settings[member.guild.id]
        if not settings.get('enabled', True):
            return
        
        channel = self.bot.get_channel(settings['channel_id'])
        if not channel:
            return
        
        # Replace variables
        def replace_vars(text):
            return text.format(
                user=member.name,
                username=member.name,
                server=member.guild.name,
                count=member.guild.member_count,
                tag=member.discriminator,
                id=member.id
            )
        
        title = replace_vars(settings.get('title', 'Goodbye!'))
        description = replace_vars(settings.get('description', '{user} has left the server.'))
        
        # Create goodbye embed
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.from_rgb(240, 71, 71)
        )
        
        embed.add_field(
            name="👤 Member Info",
            value=f"**Name:** {member.name}#{member.discriminator}\n**ID:** `{member.id}`",
            inline=False
        )
        
        time_in_server = (datetime.now() - member.joined_at).days
        embed.add_field(
            name="⏱️ Time in Server",
            value=f"**Days:** {time_in_server}\n**Joined:** {member.joined_at.strftime('%B %d, %Y')}",
            inline=False
        )
        
        embed.add_field(
            name="👥 Server Members",
            value=f"**Remaining:** {member.guild.member_count}",
            inline=False
        )
        
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        if settings.get('image_url'):
            embed.set_image(url=settings['image_url'])
        
        embed.set_footer(
            text=f"TableMC Development • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            icon_url=member.guild.icon.url if member.guild.icon else None
        )
        
        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            pass
    
    @commands.group(name='welcome', invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def welcome(self, ctx):
        """Welcome system commands"""
        embed = discord.Embed(
            title="Welcome System",
            description="Configure Sapphire-style welcome messages",
            color=discord.Color.blue()
        )
        embed.add_field(name="`!welcome channel <#channel>`", value="Set welcome channel", inline=False)
        embed.add_field(name="`!welcome title <text>`", value="Set welcome title", inline=False)
        embed.add_field(name="`!welcome description <text>`", value="Set welcome description", inline=False)
        embed.add_field(name="`!welcome image <url>`", value="Set welcome image", inline=False)
        embed.add_field(name="`!welcome test`", value="Test welcome message", inline=False)
        embed.add_field(name="`!welcome toggle`", value="Toggle welcome on/off", inline=False)
        embed.add_field(name="`!welcome preview`", value="Preview current settings", inline=False)
        embed.add_field(name="**Variables:** `{user}` `{username}` `{server}` `{count}` `{id}` `{tag}`", value="Use in title/description", inline=False)
        
        await ctx.send(embed=embed)
    
    @welcome.command(name='channel')
    async def welcome_channel(self, ctx, channel: discord.TextChannel):
        """Set welcome channel"""
        if ctx.guild.id not in self.welcome_settings:
            self.welcome_settings[ctx.guild.id] = {}
        
        self.welcome_settings[ctx.guild.id]['channel_id'] = channel.id
        self.welcome_settings[ctx.guild.id]['enabled'] = True
        
        embed = discord.Embed(
            title="✅ Welcome Channel Set",
            description=f"Welcome messages will be sent to {channel.mention}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @welcome.command(name='title')
    async def welcome_title(self, ctx, *, title):
        """Set welcome title"""
        if ctx.guild.id not in self.welcome_settings:
            self.welcome_settings[ctx.guild.id] = {}
        
        self.welcome_settings[ctx.guild.id]['title'] = title
        
        embed = discord.Embed(
            title="✅ Welcome Title Set",
            description=f"Title: `{title}`",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @welcome.command(name='description')
    async def welcome_description(self, ctx, *, description):
        """Set welcome description"""
        if ctx.guild.id not in self.welcome_settings:
            self.welcome_settings[ctx.guild.id] = {}
        
        self.welcome_settings[ctx.guild.id]['description'] = description
        
        embed = discord.Embed(
            title="✅ Welcome Description Set",
            description=f"Description: `{description}`",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @welcome.command(name='image')
    async def welcome_image(self, ctx, image_url: str):
        """Set welcome image URL"""
        if ctx.guild.id not in self.welcome_settings:
            self.welcome_settings[ctx.guild.id] = {}
        
        self.welcome_settings[ctx.guild.id]['image_url'] = image_url
        
        embed = discord.Embed(
            title="✅ Welcome Image Set",
            color=discord.Color.green()
        )
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)
    
    @welcome.command(name='test')
    async def welcome_test(self, ctx):
        """Test welcome message"""
        if ctx.guild.id not in self.welcome_settings or 'channel_id' not in self.welcome_settings[ctx.guild.id]:
            embed = discord.Embed(
                title="❌ Error",
                description="Please set a welcome channel first using `!welcome channel <#channel>`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        settings = self.welcome_settings[ctx.guild.id]
        channel = self.bot.get_channel(settings['channel_id'])
        
        if not channel:
            await ctx.send("❌ Welcome channel not found!")
            return
        
        # Replace variables
        def replace_vars(text):
            return text.format(
                user=ctx.author.mention,
                username=ctx.author.name,
                server=ctx.guild.name,
                count=ctx.guild.member_count,
                tag=ctx.author.discriminator,
                id=ctx.author.id
            )
        
        title = replace_vars(settings.get('title', 'Welcome to {server}!'))
        description = replace_vars(settings.get('description', 'Welcome {user}!'))
        
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.from_rgb(88, 165, 252)
        )
        
        embed.add_field(
            name="👤 Member Info",
            value=f"**Name:** {ctx.author.mention}\n**Tag:** {ctx.author.name}#{ctx.author.discriminator}\n**ID:** `{ctx.author.id}`",
            inline=False
        )
        
        created_days = (datetime.now() - ctx.author.created_at).days
        embed.add_field(
            name="📅 Account Info",
            value=f"**Created:** {ctx.author.created_at.strftime('%B %d, %Y')}\n**Age:** {created_days} days old",
            inline=False
        )
        
        embed.add_field(
            name="👥 Server Info",
            value=f"**Members:** {ctx.guild.member_count}\n**Joined as:** Member #{ctx.guild.member_count}",
            inline=False
        )
        
        embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else None)
        if settings.get('image_url'):
            embed.set_image(url=settings['image_url'])
        
        embed.set_footer(
            text=f"TableMC Development • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            icon_url=ctx.guild.icon.url if ctx.guild.icon else None
        )
        
        try:
            await channel.send(f"Welcome {ctx.author.mention}!", embed=embed)
            await ctx.send("✅ Test welcome message sent to the channel!")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to send messages in that channel!")
    
    @welcome.command(name='toggle')
    async def welcome_toggle(self, ctx):
        """Toggle welcome messages on/off"""
        if ctx.guild.id not in self.welcome_settings:
            await ctx.send("❌ No welcome message configured yet!")
            return
        
        current = self.welcome_settings[ctx.guild.id].get('enabled', True)
        self.welcome_settings[ctx.guild.id]['enabled'] = not current
        
        status = "✅ enabled" if not current else "❌ disabled"
        embed = discord.Embed(
            title="Welcome System",
            description=f"Welcome messages are now {status}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @welcome.command(name='preview')
    async def welcome_preview(self, ctx):
        """Preview current welcome settings"""
        if ctx.guild.id not in self.welcome_settings:
            await ctx.send("❌ No welcome settings configured!")
            return
        
        settings = self.welcome_settings[ctx.guild.id]
        
        embed = discord.Embed(
            title="Welcome Settings Preview",
            color=discord.Color.blue()
        )
        embed.add_field(name="Channel", value=f"<#{settings.get('channel_id', 'Not set')}>", inline=False)
        embed.add_field(name="Title", value=f"`{settings.get('title', 'Not set')}`", inline=False)
        embed.add_field(name="Description", value=f"`{settings.get('description', 'Not set')}`", inline=False)
        embed.add_field(name="Status", value="✅ Enabled" if settings.get('enabled', True) else "❌ Disabled", inline=False)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(SapphireWelcomer(bot))
