import discord
from discord.ext import commands
from datetime import datetime
import psutil
import os

class Utility(commands.Cog):
    """Utility and info commands"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='ping', help='Check bot latency')
    async def ping(self, ctx):
        """Check bot ping/latency"""
        latency = round(self.bot.latency * 1000)
        
        embed = discord.Embed(
            title='🏓 Pong!',
            description=f'Latency: **{latency}ms**',
            color=discord.Color.blue()
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='botinfo', help='Get bot information')
    async def botinfo(self, ctx):
        """Get information about the bot"""
        embed = discord.Embed(
            title='🤖 Bot Information',
            color=discord.Color.purple()
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)
        embed.add_field(name='Bot Name', value=self.bot.user.name, inline=True)
        embed.add_field(name='Bot ID', value=self.bot.user.id, inline=True)
        embed.add_field(name='Prefix', value='`!`', inline=True)
        embed.add_field(name='Servers', value=len(self.bot.guilds), inline=True)
        embed.add_field(name='Users', value=sum(len(guild.members) for guild in self.bot.guilds), inline=True)
        embed.add_field(name='Latency', value=f'{round(self.bot.latency * 1000)}ms', inline=True)
        embed.add_field(name='Created', value=self.bot.user.created_at.strftime('%Y-%m-%d'), inline=True)
        embed.add_field(name='Discord.py Version', value=discord.__version__, inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='serverinfo', help='Get server information')
    async def serverinfo(self, ctx):
        """Get server information"""
        guild = ctx.guild
        
        embed = discord.Embed(
            title=f'📊 {guild.name} Information',
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name='Server ID', value=guild.id, inline=True)
        embed.add_field(name='Owner', value=guild.owner.mention, inline=True)
        embed.add_field(name='Region', value=guild.region, inline=True)
        embed.add_field(name='Members', value=f'👥 {guild.member_count}', inline=True)
        embed.add_field(name='Channels', value=f'📝 {len(guild.channels)}', inline=True)
        embed.add_field(name='Roles', value=f'🏷️ {len(guild.roles)}', inline=True)
        embed.add_field(name='Created', value=guild.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
        embed.add_field(name='Verification Level', value=str(guild.verification_level).title(), inline=True)
        embed.add_field(name='Content Filter', value=str(guild.explicit_content_filter).title(), inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='userinfo', help='Get user information')
    async def userinfo(self, ctx, member: discord.Member = None):
        """Get user information"""
        if member is None:
            member = ctx.author
        
        embed = discord.Embed(
            title=f'👤 {member.name}\'s Information',
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        embed.add_field(name='User ID', value=member.id, inline=True)
        embed.add_field(name='Username', value=member.name, inline=True)
        embed.add_field(name='Discriminator', value=f'#{member.discriminator}', inline=True)
        embed.add_field(name='Account Created', value=member.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
        embed.add_field(name='Joined Server', value=member.joined_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
        embed.add_field(name='Roles', value=', '.join([role.mention for role in member.roles[1:]]) or 'No roles', inline=False)
        embed.add_field(name='Status', value=f'🟢 {member.status}' if member.status else '⚫ Offline', inline=True)
        embed.add_field(name='Bot', value='✓ Yes' if member.bot else '✗ No', inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='avatar', help='Get user avatar')
    async def avatar(self, ctx, member: discord.Member = None):
        """Get user avatar"""
        if member is None:
            member = ctx.author
        
        if not member.avatar:
            await ctx.send('❌ User has no avatar!')
            return
        
        embed = discord.Embed(
            title=f'{member.name}\'s Avatar',
            color=discord.Color.blue()
        )
        embed.set_image(url=member.avatar.url)
        embed.add_field(name='Download', value=f'[PNG]({member.avatar.url}?size=1024)')
        
        await ctx.send(embed=embed)
    
    @commands.command(name='stats', help='Get bot statistics')
    async def stats(self, ctx):
        """Get bot statistics"""
        process = psutil.Process(os.getpid())
        memory_usage = process.memory_info().rss / 1024 / 1024
        cpu_usage = process.cpu_percent()
        
        embed = discord.Embed(
            title='📈 Bot Statistics',
            color=discord.Color.green()
        )
        embed.add_field(name='Memory Usage', value=f'{memory_usage:.2f} MB', inline=True)
        embed.add_field(name='CPU Usage', value=f'{cpu_usage:.2f}%', inline=True)
        embed.add_field(name='Servers', value=len(self.bot.guilds), inline=True)
        embed.add_field(name='Users', value=sum(len(guild.members) for guild in self.bot.guilds), inline=True)
        embed.add_field(name='Channels', value=sum(len(guild.channels) for guild in self.bot.guilds), inline=True)
        embed.add_field(name='Latency', value=f'{round(self.bot.latency * 1000)}ms', inline=True)
        embed.set_footer(text=f'Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        
        await ctx.send(embed=embed)
    
    @commands.command(name='invite', help='Get bot invite link')
    async def invite(self, ctx):
        """Get bot invite link"""
        permissions = discord.Permissions(
            administrator=True,
            manage_guild=True,
            manage_channels=True,
            manage_roles=True,
            kick_members=True,
            ban_members=True,
            manage_messages=True,
            embed_links=True,
            attach_files=True,
            read_message_history=True
        )
        
        invite_url = discord.utils.oauth_url(self.bot.user.id, permissions=permissions)
        
        embed = discord.Embed(
            title='🔗 Bot Invite Link',
            description=f'[Invite Bot]({invite_url})',
            color=discord.Color.blue()
        )
        embed.add_field(name='Permissions', value='✓ Administrator', inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='help', help='Show help information')
    async def help_command(self, ctx):
        """Show help information"""
        embed = discord.Embed(
            title='📚 Bot Help',
            description='List of available commands',
            color=discord.Color.blue()
        )
        
        # Group commands by cog
        for cog_name, cog in self.bot.cogs.items():
            commands_list = cog.get_commands()
            if commands_list:
                command_names = ', '.join([f'`{cmd.name}`' for cmd in commands_list])
                embed.add_field(name=f'**{cog_name}**', value=command_names, inline=False)
        
        embed.set_footer(text='Use !command help for more info on a specific command')
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))
