import discord
from discord.ext import commands
from datetime import datetime
import random

class Leveling(commands.Cog):
    """Leveling system for users"""
    
    def __init__(self, bot):
        self.bot = bot
        self.user_data = {}  # {user_id: {'level': int, 'xp': int, 'total_xp': int}}
        self.cooldown = {}  # {user_id: timestamp}
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Award XP for messages"""
        if message.author.bot or not message.guild:
            return
        
        user_id = message.author.id
        current_time = datetime.now().timestamp()
        
        # Check cooldown (5 seconds between XP gains)
        if user_id in self.cooldown:
            if current_time - self.cooldown[user_id] < 5:
                return
        
        # Initialize user data if not exists
        if user_id not in self.user_data:
            self.user_data[user_id] = {'level': 1, 'xp': 0, 'total_xp': 0}
        
        # Award XP (random between 10-25)
        xp_gained = random.randint(10, 25)
        self.user_data[user_id]['xp'] += xp_gained
        self.user_data[user_id]['total_xp'] += xp_gained
        
        # Check for level up
        xp_required = 100 * self.user_data[user_id]['level']
        
        if self.user_data[user_id]['xp'] >= xp_required:
            self.user_data[user_id]['level'] += 1
            self.user_data[user_id]['xp'] = 0
            
            embed = discord.Embed(
                title='🎉 Level Up!',
                description=f'{message.author.mention} reached level {self.user_data[user_id]["level"]}!',
                color=discord.Color.gold()
            )
            embed.set_thumbnail(url=message.author.avatar.url if message.author.avatar else None)
            
            await message.channel.send(embed=embed)
        
        self.cooldown[user_id] = current_time
    
    @commands.command(name='level', help='Check your or someone else\'s level')
    async def level(self, ctx, member: discord.Member = None):
        """Check user level"""
        if member is None:
            member = ctx.author
        
        user_id = member.id
        
        if user_id not in self.user_data:
            self.user_data[user_id] = {'level': 1, 'xp': 0, 'total_xp': 0}
        
        data = self.user_data[user_id]
        xp_required = 100 * data['level']
        xp_percent = (data['xp'] / xp_required) * 100
        
        embed = discord.Embed(
            title=f'{member.name}\'s Level',
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        embed.add_field(name='Level', value=f'**{data["level"]}**', inline=True)
        embed.add_field(name='Total XP', value=f'**{data["total_xp"]}**', inline=True)
        embed.add_field(name='Current XP', value=f'**{data["xp"]}/{xp_required}** ({xp_percent:.1f}%)', inline=False)
        
        # Progress bar
        bar_length = 20
        filled = int(bar_length * (data['xp'] / xp_required))
        bar = '█' * filled + '░' * (bar_length - filled)
        embed.add_field(name='Progress', value=f'`{bar}`', inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='leaderboard', help='View server leaderboard')
    async def leaderboard(self, ctx):
        """View leaderboard"""
        if not self.user_data:
            await ctx.send('❌ No users have leveled up yet!')
            return
        
        # Sort by level and total_xp
        sorted_users = sorted(
            self.user_data.items(),
            key=lambda x: (x[1]['level'], x[1]['total_xp']),
            reverse=True
        )[:10]
        
        embed = discord.Embed(
            title='🏆 Level Leaderboard',
            description='Top 10 members by level',
            color=discord.Color.gold()
        )
        
        for i, (user_id, data) in enumerate(sorted_users, 1):
            try:
                user = await self.bot.fetch_user(user_id)
                embed.add_field(
                    name=f'#{i} - {user.name}',
                    value=f'Level **{data["level"]}** | XP: **{data["total_xp"]}**',
                    inline=False
                )
            except:
                pass
        
        await ctx.send(embed=embed)
    
    @commands.command(name='addxp', help='Add XP to a user (Admin only)')
    @commands.has_permissions(administrator=True)
    async def addxp(self, ctx, member: discord.Member, amount: int):
        """Add XP to a user"""
        user_id = member.id
        
        if user_id not in self.user_data:
            self.user_data[user_id] = {'level': 1, 'xp': 0, 'total_xp': 0}
        
        self.user_data[user_id]['xp'] += amount
        self.user_data[user_id]['total_xp'] += amount
        
        embed = discord.Embed(
            title='✓ XP Added',
            description=f'Added {amount} XP to {member.mention}',
            color=discord.Color.green()
        )
        embed.add_field(name='New Total XP', value=self.user_data[user_id]['total_xp'])
        
        await ctx.send(embed=embed)
    
    @commands.command(name='resetxp', help='Reset XP for a user (Admin only)')
    @commands.has_permissions(administrator=True)
    async def resetxp(self, ctx, member: discord.Member):
        """Reset user XP"""
        user_id = member.id
        
        if user_id in self.user_data:
            self.user_data[user_id] = {'level': 1, 'xp': 0, 'total_xp': 0}
            await ctx.send(f'✓ XP reset for {member.mention}')
        else:
            await ctx.send(f'{member.mention} has no XP data to reset')

async def setup(bot):
    await bot.add_cog(Leveling(bot))
