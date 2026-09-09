import discord
from discord.ext import commands
from datetime import datetime, timedelta
import json

class AdvancedModeration(commands.Cog):
    """Advanced moderation system with logging"""
    
    def __init__(self, bot):
        self.bot = bot
        self.warnings = {}  # {user_id: [(reason, timestamp, moderator_id)]}
        self.mutes = {}  # {user_id: {end_time, reason}}
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """Log member changes"""
        if before.roles != after.roles:
            added_roles = set(after.roles) - set(before.roles)
            removed_roles = set(before.roles) - set(after.roles)
            
            if added_roles or removed_roles:
                log_embed = discord.Embed(
                    title="👤 Member Roles Updated",
                    color=discord.Color.blue()
                )
                log_embed.add_field(name="Member", value=f"{after.mention} ({after.id})", inline=False)
                if added_roles:
                    log_embed.add_field(name="Added", value=", ".join([r.mention for r in added_roles]), inline=False)
                if removed_roles:
                    log_embed.add_field(name="Removed", value=", ".join([r.mention for r in removed_roles]), inline=False)
                log_embed.set_footer(text=f"ID: {after.id} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Send to mod log channel if exists
                await self.log_action(after.guild, log_embed)
    
    async def log_action(self, guild, embed):
        """Send log to moderation channel"""
        # Look for #mod-log or similar channel
        for channel in guild.text_channels:
            if 'mod' in channel.name or 'log' in channel.name:
                try:
                    await channel.send(embed=embed)
                    return
                except discord.Forbidden:
                    pass
    
    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Kick a member from the server"""
        if member == ctx.author:
            await ctx.send("❌ You cannot kick yourself!")
            return
        
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ You cannot kick someone with equal or higher role!")
            return
        
        try:
            await member.send(
                embed=discord.Embed(
                    title="🚨 You were kicked",
                    description=f"**Server:** {ctx.guild.name}\n**Reason:** {reason}",
                    color=discord.Color.red()
                )
            )
        except:
            pass
        
        await member.kick(reason=reason)
        
        embed = discord.Embed(
            title="🚨 Member Kicked",
            color=discord.Color.red()
        )
        embed.add_field(name="Member", value=f"{member.mention} ({member.id})", inline=False)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        await ctx.send(embed=embed)
        await self.log_action(ctx.guild, embed)
    
    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Ban a member from the server"""
        if member == ctx.author:
            await ctx.send("❌ You cannot ban yourself!")
            return
        
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ You cannot ban someone with equal or higher role!")
            return
        
        try:
            await member.send(
                embed=discord.Embed(
                    title="⛔ You were banned",
                    description=f"**Server:** {ctx.guild.name}\n**Reason:** {reason}",
                    color=discord.Color.red()
                )
            )
        except:
            pass
        
        await member.ban(reason=reason)
        
        embed = discord.Embed(
            title="⛔ Member Banned",
            color=discord.Color.red()
        )
        embed.add_field(name="Member", value=f"{member.mention} ({member.id})", inline=False)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        await ctx.send(embed=embed)
        await self.log_action(ctx.guild, embed)
    
    @commands.command(name='warn')
    @commands.has_permissions(moderate_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Warn a member (3 warnings = kick)"""
        user_id = member.id
        
        if user_id not in self.warnings:
            self.warnings[user_id] = []
        
        self.warnings[user_id].append((reason, datetime.now(), ctx.author.id))
        warn_count = len(self.warnings[user_id])
        
        embed = discord.Embed(
            title="⚠️ Member Warned",
            color=discord.Color.orange()
        )
        embed.add_field(name="Member", value=f"{member.mention} ({member.id})", inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Warnings", value=f"{warn_count}/3", inline=True)
        embed.set_footer(text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        await ctx.send(embed=embed)
        await self.log_action(ctx.guild, embed)
        
        # Auto-kick after 3 warnings
        if warn_count >= 3:
            try:
                await member.kick(reason="Automatic kick: 3 warnings")
                await ctx.send(f"🚨 {member.mention} has been automatically kicked for 3 warnings!")
            except:
                pass
    
    @commands.command(name='mute')
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, duration: int = 10, *, reason="No reason provided"):
        """Mute a member (duration in minutes)"""
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        
        if not mute_role:
            mute_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, send_messages=False, speak=False)
        
        await member.add_roles(mute_role)
        
        self.mutes[member.id] = {
            'end_time': datetime.now() + timedelta(minutes=duration),
            'reason': reason
        }
        
        embed = discord.Embed(
            title="🔇 Member Muted",
            color=discord.Color.orange()
        )
        embed.add_field(name="Member", value=f"{member.mention} ({member.id})", inline=False)
        embed.add_field(name="Duration", value=f"{duration} minutes", inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        await ctx.send(embed=embed)
        await self.log_action(ctx.guild, embed)
    
    @commands.command(name='unmute')
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member):
        """Unmute a member"""
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        
        if mute_role in member.roles:
            await member.remove_roles(mute_role)
            
            embed = discord.Embed(
                title="🔊 Member Unmuted",
                color=discord.Color.green()
            )
            embed.add_field(name="Member", value=f"{member.mention} ({member.id})", inline=False)
            embed.set_footer(text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            
            await ctx.send(embed=embed)
            await self.log_action(ctx.guild, embed)
        else:
            await ctx.send("❌ This member is not muted!")
    
    @commands.command(name='purge')
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = 10):
        """Delete multiple messages"""
        if amount > 100:
            await ctx.send("❌ Cannot delete more than 100 messages at once!")
            return
        
        deleted = await ctx.channel.purge(limit=amount + 1)
        
        embed = discord.Embed(
            title="🗑️ Messages Purged",
            description=f"Deleted {len(deleted) - 1} messages",
            color=discord.Color.red()
        )
        embed.add_field(name="Channel", value=ctx.channel.mention, inline=False)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)
        embed.set_footer(text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        await ctx.send(embed=embed, delete_after=10)

async def setup(bot):
    await bot.add_cog(AdvancedModeration(bot))
