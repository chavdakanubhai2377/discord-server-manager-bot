import discord
from discord.ext import commands
from datetime import datetime
import json

class PremiumTickets(commands.Cog):
    """Premium ticket system (Roti bot style) with interactive embeds"""
    
    def __init__(self, bot):
        self.bot = bot
        self.ticket_settings = {}  # {guild_id: {category_id, support_role_id, enabled}}
        self.active_tickets = {}  # {ticket_channel_id: {user_id, created_at, status}}
    
    @commands.group(name='ticket', invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def ticket(self, ctx):
        """Ticket system commands"""
        embed = discord.Embed(
            title="🎫 Premium Ticket System",
            description="TableMC Development - Roti Bot Style",
            color=discord.Color.from_rgb(88, 165, 252)
        )
        embed.add_field(name="`!ticket setup <category> <role>`", value="Setup ticket system", inline=False)
        embed.add_field(name="`!ticket create`", value="Create a support ticket", inline=False)
        embed.add_field(name="`!ticket close`", value="Close current ticket", inline=False)
        embed.add_field(name="`!ticket reopen`", value="Reopen a ticket", inline=False)
        embed.add_field(name="`!ticket panel`", value="Send ticket creation panel", inline=False)
        embed.add_field(name="`!ticket status`", value="Check ticket status", inline=False)
        embed.set_footer(text="TableMC Development • Ticket System", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
        
        await ctx.send(embed=embed)
    
    @ticket.command(name='setup')
    @commands.has_permissions(manage_guild=True)
    async def ticket_setup(self, ctx, category: discord.CategoryChannel, support_role: discord.Role):
        """Setup ticket system"""
        self.ticket_settings[ctx.guild.id] = {
            'category_id': category.id,
            'support_role_id': support_role.id,
            'enabled': True
        }
        
        embed = discord.Embed(
            title="✅ Ticket System Setup Complete",
            color=discord.Color.green()
        )
        embed.add_field(name="Category", value=category.mention, inline=True)
        embed.add_field(name="Support Role", value=support_role.mention, inline=True)
        embed.add_field(name="Status", value="✅ Enabled", inline=True)
        embed.add_field(name="Next Step", value="Use `!ticket panel` to create the ticket creation panel", inline=False)
        
        await ctx.send(embed=embed)
    
    @ticket.command(name='panel')
    @commands.has_permissions(manage_guild=True)
    async def ticket_panel(self, ctx):
        """Send ticket creation panel"""
        if ctx.guild.id not in self.ticket_settings:
            embed = discord.Embed(
                title="❌ Error",
                description="Ticket system not setup! Use `!ticket setup` first",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(
            title="🎫 Support Ticket System",
            description="Click the button below to create a support ticket.\n\nOur support team will assist you as soon as possible!",
            color=discord.Color.from_rgb(88, 165, 252)
        )
        embed.add_field(name="⏱️ Response Time", value="Usually within 24 hours", inline=True)
        embed.add_field(name="✅ Available", value="24/7 Support", inline=True)
        embed.set_footer(text="TableMC Development • Support System", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
        
        view = TicketPanelView(self.bot, self)
        await ctx.send(embed=embed, view=view)
    
    @ticket.command(name='create')
    async def ticket_create(self, ctx):
        """Create a support ticket"""
        if ctx.guild.id not in self.ticket_settings:
            embed = discord.Embed(
                title="❌ Error",
                description="Ticket system not configured",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        settings = self.ticket_settings[ctx.guild.id]
        category = ctx.guild.get_channel(settings['category_id'])
        support_role = ctx.guild.get_role(settings['support_role_id'])
        
        if not category or not support_role:
            await ctx.send("❌ Ticket system not properly configured")
            return
        
        # Check if user already has a ticket
        for channel in category.channels:
            if isinstance(channel, discord.TextChannel) and ctx.author.id in [m.id for m in channel.members]:
                embed = discord.Embed(
                    title="❌ You Already Have a Ticket",
                    description=f"You already have an open ticket: {channel.mention}",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed, delete_after=10)
                return
        
        # Create ticket channel
        ticket_num = len(category.channels) + 1
        channel_name = f"ticket-{ctx.author.name}-{ticket_num}"
        
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            ctx.author: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            support_role: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            self.bot.user: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }
        
        ticket_channel = await category.create_text_channel(channel_name, overwrites=overwrites)
        
        # Store ticket info
        self.active_tickets[ticket_channel.id] = {
            'user_id': ctx.author.id,
            'created_at': datetime.now(),
            'status': 'open'
        }
        
        # Send welcome embed
        embed = discord.Embed(
            title="🎫 Support Ticket Created",
            description=f"Thank you for reaching out, {ctx.author.mention}!\n\nOur support team will respond shortly.",
            color=discord.Color.from_rgb(88, 165, 252)
        )
        embed.add_field(name="Ticket ID", value=f"`{ticket_channel.id}`", inline=True)
        embed.add_field(name="Status", value="🟢 Open", inline=True)
        embed.add_field(name="Support Team", value=support_role.mention, inline=False)
        embed.add_field(name="How to Close", value="React with 🔒 or use `!ticket close`", inline=False)
        embed.set_footer(text="TableMC Development • Support System", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
        
        message = await ticket_channel.send(embed=embed)
        await message.add_reaction('🔒')
        
        # Notify user
        try:
            dm_embed = discord.Embed(
                title="✅ Ticket Created",
                description=f"Your support ticket has been created in {ctx.guild.name}",
                color=discord.Color.green()
            )
            await ctx.author.send(embed=dm_embed)
        except:
            pass
        
        # Confirm in original channel
        confirm_embed = discord.Embed(
            title="✅ Ticket Created",
            description=f"Your support ticket has been created: {ticket_channel.mention}",
            color=discord.Color.green()
        )
        await ctx.send(embed=confirm_embed, delete_after=10)
    
    @ticket.command(name='close')
    async def ticket_close(self, ctx):
        """Close a ticket"""
        if ctx.channel.id not in self.active_tickets:
            await ctx.send("❌ This is not a ticket channel!")
            return
        
        ticket_info = self.active_tickets[ctx.channel.id]
        
        # Create transcript
        messages = []
        async for message in ctx.channel.history(limit=100, oldest_first=True):
            messages.append(f"[{message.created_at}] {message.author}: {message.content}")
        
        transcript = "\n".join(messages)
        
        # Update status
        self.active_tickets[ctx.channel.id]['status'] = 'closed'
        
        # Send closing embed
        embed = discord.Embed(
            title="🔒 Ticket Closed",
            description=f"This ticket has been closed by {ctx.author.mention}",
            color=discord.Color.orange()
        )
        embed.add_field(name="Created", value=ticket_info['created_at'].strftime('%Y-%m-%d %H:%M:%S'), inline=True)
        embed.add_field(name="Closed", value=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), inline=True)
        embed.add_field(name="Duration", value=f"{(datetime.now() - ticket_info['created_at']).days} days", inline=True)
        embed.set_footer(text="Channel will be deleted in 10 seconds")
        
        await ctx.send(embed=embed)
        
        # Wait and delete
        await asyncio.sleep(10)
        await ctx.channel.delete()
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """Handle ticket close reaction"""
        if reaction.emoji == '🔒' and reaction.message.channel.id in self.active_tickets:
            if self.active_tickets[reaction.message.channel.id]['status'] == 'open':
                self.active_tickets[reaction.message.channel.id]['status'] = 'closed'
                
                embed = discord.Embed(
                    title="🔒 Ticket Closed",
                    description=f"This ticket has been closed by {user.mention}",
                    color=discord.Color.orange()
                )
                embed.set_footer(text="Channel will be deleted in 10 seconds")
                
                await reaction.message.channel.send(embed=embed)
                
                import asyncio
                await asyncio.sleep(10)
                await reaction.message.channel.delete()

class TicketPanelView(discord.ui.View):
    def __init__(self, bot, cog):
        super().__init__(timeout=None)
        self.bot = bot
        self.cog = cog
    
    @discord.ui.button(label="Create Support Ticket", style=discord.ButtonStyle.primary, emoji="🎫")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Create ticket button"""
        if interaction.guild.id not in self.cog.ticket_settings:
            await interaction.response.send_message("❌ Ticket system not configured", ephemeral=True)
            return
        
        settings = self.cog.ticket_settings[interaction.guild.id]
        category = interaction.guild.get_channel(settings['category_id'])
        support_role = interaction.guild.get_role(settings['support_role_id'])
        
        # Check if user already has a ticket
        for channel in category.channels:
            if isinstance(channel, discord.TextChannel) and interaction.user.id in [m.id for m in channel.members]:
                embed = discord.Embed(
                    title="❌ You Already Have a Ticket",
                    description=f"You already have an open ticket: {channel.mention}",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
        
        # Create ticket channel
        ticket_num = len(category.channels) + 1
        channel_name = f"ticket-{interaction.user.name}-{ticket_num}"
        
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            support_role: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            self.bot.user: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }
        
        ticket_channel = await category.create_text_channel(channel_name, overwrites=overwrites)
        
        # Store ticket info
        self.cog.active_tickets[ticket_channel.id] = {
            'user_id': interaction.user.id,
            'created_at': datetime.now(),
            'status': 'open'
        }
        
        # Send welcome embed
        embed = discord.Embed(
            title="🎫 Support Ticket Created",
            description=f"Thank you for reaching out, {interaction.user.mention}!\n\nOur support team will respond shortly.",
            color=discord.Color.from_rgb(88, 165, 252)
        )
        embed.add_field(name="Ticket ID", value=f"`{ticket_channel.id}`", inline=True)
        embed.add_field(name="Status", value="🟢 Open", inline=True)
        embed.add_field(name="Support Team", value=support_role.mention, inline=False)
        embed.add_field(name="How to Close", value="React with 🔒 or use `!ticket close`", inline=False)
        embed.set_footer(text="TableMC Development • Support System", icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
        
        message = await ticket_channel.send(embed=embed)
        await message.add_reaction('🔒')
        
        confirm_embed = discord.Embed(
            title="✅ Ticket Created",
            description=f"Your support ticket: {ticket_channel.mention}",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=confirm_embed, ephemeral=True)

import asyncio

async def setup(bot):
    await bot.add_cog(PremiumTickets(bot))
