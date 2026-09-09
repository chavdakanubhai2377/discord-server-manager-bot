import discord
from discord.ext import commands
from datetime import datetime

class ReactionRoles(commands.Cog):
    """Reaction role system for automatic role assignment via reactions"""
    
    def __init__(self, bot):
        self.bot = bot
        self.reaction_roles = {}  # {message_id: {emoji: role_id}}
        self.reaction_messages = {}  # {guild_id: [message_id]}
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Handle reaction addition"""
        if payload.message_id not in self.reaction_roles:
            return
        
        emoji = str(payload.emoji)
        
        if emoji not in self.reaction_roles[payload.message_id]:
            return
        
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role_id = self.reaction_roles[payload.message_id][emoji]
        role = guild.get_role(role_id)
        
        if member and role:
            try:
                await member.add_roles(role)
            except discord.Forbidden:
                pass
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """Handle reaction removal"""
        if payload.message_id not in self.reaction_roles:
            return
        
        emoji = str(payload.emoji)
        
        if emoji not in self.reaction_roles[payload.message_id]:
            return
        
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role_id = self.reaction_roles[payload.message_id][emoji]
        role = guild.get_role(role_id)
        
        if member and role:
            try:
                await member.remove_roles(role)
            except discord.Forbidden:
                pass
    
    @commands.group(name='reactionrole', invoke_without_command=True)
    @commands.has_permissions(manage_roles=True)
    async def reactionrole(self, ctx):
        """Reaction role system commands"""
        embed = discord.Embed(
            title="🎭 Reaction Role System",
            description="Automatic role assignment via reactions",
            color=discord.Color.blue()
        )
        embed.add_field(name="`!reactionrole create <title>`", value="Create new reaction role message", inline=False)
        embed.add_field(name="`!reactionrole add <message_id> <emoji> <role>`", value="Add reaction-role pair", inline=False)
        embed.add_field(name="`!reactionrole remove <message_id> <emoji>`", value="Remove reaction-role pair", inline=False)
        embed.add_field(name="`!reactionrole list [message_id]`", value="List all reaction roles", inline=False)
        embed.add_field(name="`!reactionrole delete <message_id>`", value="Delete reaction role message", inline=False)
        embed.set_footer(text="TableMC Development • Reaction Roles", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
        
        await ctx.send(embed=embed)
    
    @reactionrole.command(name='create')
    async def create_reaction_message(self, ctx, *, title: str = "React to get roles"):
        """Create a new reaction role message"""
        embed = discord.Embed(
            title="🎭 " + title,
            description="React to this message to get roles!\n\nClick on the reactions below to assign roles to yourself.",
            color=discord.Color.from_rgb(88, 165, 252)
        )
        embed.add_field(name="How it works", value="1. React with the emoji\n2. You'll automatically get the role\n3. Remove reaction to remove role", inline=False)
        embed.set_footer(text="TableMC Development • Reaction Roles", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
        
        message = await ctx.send(embed=embed)
        
        # Store message ID
        self.reaction_roles[message.id] = {}
        if ctx.guild.id not in self.reaction_messages:
            self.reaction_messages[ctx.guild.id] = []
        self.reaction_messages[ctx.guild.id].append(message.id)
        
        confirm_embed = discord.Embed(
            title="✅ Reaction Role Message Created",
            description=f"Message ID: `{message.id}`\n\nUse `!reactionrole add {message.id} <emoji> <role>` to add roles",
            color=discord.Color.green()
        )
        await ctx.send(embed=confirm_embed)
    
    @reactionrole.command(name='add')
    async def add_reaction_role(self, ctx, message_id: int, emoji: str, role: discord.Role):
        """Add a reaction-role pair"""
        if message_id not in self.reaction_roles:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Message ID `{message_id}` not found!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        # Try to get the message
        try:
            message = await ctx.channel.fetch_message(message_id)
        except discord.NotFound:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Message `{message_id}` not found in this channel!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        # Validate emoji
        try:
            await message.add_reaction(emoji)
        except discord.InvalidArgument:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Invalid emoji: `{emoji}`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Error",
                description="I don't have permission to add reactions!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        # Add to database
        self.reaction_roles[message_id][emoji] = role.id
        
        embed = discord.Embed(
            title="✅ Reaction-Role Added",
            description=f"Emoji: {emoji}\nRole: {role.mention}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @reactionrole.command(name='remove')
    async def remove_reaction_role(self, ctx, message_id: int, emoji: str):
        """Remove a reaction-role pair"""
        if message_id not in self.reaction_roles:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Message ID `{message_id}` not found!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        if emoji not in self.reaction_roles[message_id]:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Emoji `{emoji}` not found in this message!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        role_id = self.reaction_roles[message_id].pop(emoji)
        role = ctx.guild.get_role(role_id)
        
        embed = discord.Embed(
            title="✅ Reaction-Role Removed",
            description=f"Emoji: {emoji}\nRole: {role.mention if role else 'Unknown'}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @reactionrole.command(name='list')
    async def list_reaction_roles(self, ctx, message_id: int = None):
        """List all reaction roles"""
        if message_id:
            if message_id not in self.reaction_roles:
                embed = discord.Embed(
                    title="❌ Error",
                    description=f"Message ID `{message_id}` not found!",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
            
            emoji_roles = self.reaction_roles[message_id]
            
            if not emoji_roles:
                embed = discord.Embed(
                    title="📋 Reaction Roles",
                    description="No reaction roles configured for this message",
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)
                return
            
            embed = discord.Embed(
                title=f"📋 Reaction Roles (Message {message_id})",
                description=f"Total: {len(emoji_roles)}",
                color=discord.Color.blue()
            )
            
            for emoji, role_id in emoji_roles.items():
                role = ctx.guild.get_role(role_id)
                embed.add_field(
                    name=emoji,
                    value=role.mention if role else f"Unknown Role ({role_id})",
                    inline=True
                )
            
            await ctx.send(embed=embed)
        else:
            if ctx.guild.id not in self.reaction_messages:
                embed = discord.Embed(
                    title="📋 Reaction Role Messages",
                    description="No reaction role messages created",
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)
                return
            
            embed = discord.Embed(
                title="📋 Reaction Role Messages",
                description=f"Total: {len(self.reaction_messages[ctx.guild.id])}",
                color=discord.Color.blue()
            )
            
            for msg_id in self.reaction_messages[ctx.guild.id]:
                emoji_count = len(self.reaction_roles.get(msg_id, {}))
                embed.add_field(
                    name=f"Message {msg_id}",
                    value=f"Roles: {emoji_count}",
                    inline=False
                )
            
            await ctx.send(embed=embed)
    
    @reactionrole.command(name='delete')
    async def delete_reaction_message(self, ctx, message_id: int):
        """Delete a reaction role message"""
        if message_id not in self.reaction_roles:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Message ID `{message_id}` not found!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        # Remove from storage
        del self.reaction_roles[message_id]
        
        if ctx.guild.id in self.reaction_messages:
            if message_id in self.reaction_messages[ctx.guild.id]:
                self.reaction_messages[ctx.guild.id].remove(message_id)
        
        embed = discord.Embed(
            title="✅ Reaction Role Message Deleted",
            description=f"Message ID: `{message_id}`",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @reactionrole.command(name='sync')
    async def sync_message(self, ctx, message_id: int):
        """Sync a reaction role message (add all configured reactions)"""
        if message_id not in self.reaction_roles:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Message ID `{message_id}` not found!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        try:
            message = await ctx.channel.fetch_message(message_id)
        except discord.NotFound:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Message `{message_id}` not found!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        # Clear old reactions
        try:
            await message.clear_reactions()
        except discord.Forbidden:
            pass
        
        # Add new reactions
        for emoji in self.reaction_roles[message_id].keys():
            try:
                await message.add_reaction(emoji)
            except discord.Forbidden:
                pass
        
        embed = discord.Embed(
            title="✅ Reaction Message Synced",
            description=f"Added {len(self.reaction_roles[message_id])} reactions",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
