import discord
from discord.ext import commands
from datetime import datetime, timedelta
import asyncio

class Moderation(commands.Cog):
    """Moderation commands for server management"""
    
    def __init__(self, bot):
        self.bot = bot
        self.warnings = {}  # {user_id: count}
        self.muted_users = {}  # {user_id: unmute_time}
    
    @commands.command(name='kick', help='Kick a member from the server')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kick a member from the server"""
        try:
            if member == ctx.author:
                await ctx.send('❌ You cannot kick yourself!')
                return
            
            if member.top_role >= ctx.author.top_role:
                await ctx.send('❌ You cannot kick someone with equal or higher role!')
                return
            
            await member.kick(reason=reason)
            
            embed = discord.Embed(
                title='⚠️ Member Kicked',
                description=f'{member.mention} has been kicked',
                color=discord.Color.orange()
            )
            embed.add_field(name='Reason', value=reason or 'No reason provided')
            embed.add_field(name='Kicked By', value=ctx.author.mention)
            embed.set_footer(text=f'Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send('❌ I don\'t have permission to kick this member!')
        except Exception as e:
            await ctx.send(f'❌ Error: {e}')
    
    @commands.command(name='ban', help='Ban a member from the server')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Ban a member from the server"""
        try:
            if member == ctx.author:
                await ctx.send('❌ You cannot ban yourself!')
                return
            
            if member.top_role >= ctx.author.top_role:
                await ctx.send('❌ You cannot ban someone with equal or higher role!')
                return
            
            await member.ban(reason=reason)
            
            embed = discord.Embed(
                title='🔨 Member Banned',
                description=f'{member.mention} has been banned',
                color=discord.Color.red()
            )
            embed.add_field(name='Reason', value=reason or 'No reason provided')
            embed.add_field(name='Banned By', value=ctx.author.mention)
            embed.set_footer(text=f'Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send('❌ I don\'t have permission to ban this member!')
        except Exception as e:
            await ctx.send(f'❌ Error: {e}')
    
    @commands.command(name='warn', help='Warn a member')
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        """Warn a member"""
        try:
            user_id = member.id
            
            if user_id not in self.warnings:
                self.warnings[user_id] = 0
            
            self.warnings[user_id] += 1
            warn_count = self.warnings[user_id]
            
            embed = discord.Embed(
                title='⚠️ Warning Issued',
                description=f'{member.mention} has been warned',
                color=discord.Color.yellow()
            )
            embed.add_field(name='Reason', value=reason or 'No reason provided')
            embed.add_field(name='Warning Count', value=f'{warn_count}/3')
            embed.add_field(name='Warned By', value=ctx.author.mention)
            
            await ctx.send(embed=embed)
            
            # Auto-kick after 3 warnings
            if warn_count >= 3:
                await member.kick(reason='Reached maximum warnings (3)')
                await ctx.send(f'⚠️ {member.mention} has been kicked for reaching 3 warnings!')
                self.warnings[user_id] = 0
        except Exception as e:
            await ctx.send(f'❌ Error: {e}')
    
    @commands.command(name='mute', help='Mute a member')
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, time: str = None, *, reason=None):
        """Mute a member (temporarily or permanently)"""
        try:
            # Get or create muted role
            muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
            
            if not muted_role:
                muted_role = await ctx.guild.create_role(
                    name='Muted',
                    reason='Muted role for moderation'
                )
                
                # Set permissions for all channels
                for channel in ctx.guild.channels:
                    await channel.set_permissions(
                        muted_role,
                        send_messages=False,
                        speak=False
                    )
            
            await member.add_roles(muted_role, reason=reason)
            
            embed = discord.Embed(
                title='🔇 Member Muted',
                description=f'{member.mention} has been muted',
                color=discord.Color.blue()
            )
            embed.add_field(name='Duration', value=time or 'Indefinite')
            embed.add_field(name='Reason', value=reason or 'No reason provided')
            embed.add_field(name='Muted By', value=ctx.author.mention)
            
            await ctx.send(embed=embed)
            
            # Handle temporary mute
            if time:
                await asyncio.sleep(self._parse_time(time))
                await member.remove_roles(muted_role, reason='Mute duration expired')
                await ctx.send(f'✓ {member.mention} has been unmuted!')
        
        except Exception as e:
            await ctx.send(f'❌ Error: {e}')
    
    @commands.command(name='unmute', help='Unmute a member')
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        """Unmute a member"""
        try:
            muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
            
            if not muted_role:
                await ctx.send('❌ Muted role does not exist!')
                return
            
            if muted_role not in member.roles:
                await ctx.send(f'❌ {member.mention} is not muted!')
                return
            
            await member.remove_roles(muted_role)
            
            embed = discord.Embed(
                title='🔊 Member Unmuted',
                description=f'{member.mention} has been unmuted',
                color=discord.Color.green()
            )
            embed.add_field(name='Unmuted By', value=ctx.author.mention)
            
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f'❌ Error: {e}')
    
    @commands.command(name='purge', help='Delete messages')
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = 10):
        """Delete a certain number of messages"""
        try:
            if amount > 100:
                await ctx.send('❌ Cannot delete more than 100 messages at once!')
                return
            
            deleted = await ctx.channel.purge(limit=amount + 1)
            
            embed = discord.Embed(
                title='🗑️ Messages Purged',
                description=f'Deleted {len(deleted) - 1} messages',
                color=discord.Color.purple()
            )
            embed.add_field(name='Purged By', value=ctx.author.mention)
            
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await msg.delete()
        except Exception as e:
            await ctx.send(f'❌ Error: {e}')
    
    def _parse_time(self, time_str: str) -> int:
        """Parse time string to seconds"""
        # Example: "5m" = 5 minutes, "1h" = 1 hour, "1d" = 1 day
        units = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        try:
            amount = int(time_str[:-1])
            unit = time_str[-1]
            return amount * units.get(unit, 1)
        except:
            return 0

async def setup(bot):
    await bot.add_cog(Moderation(bot))
