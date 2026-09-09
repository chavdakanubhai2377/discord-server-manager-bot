import discord
from discord.ext import commands
from datetime import datetime

class AutoResponder(commands.Cog):
    """Auto-responder system for automatic keyword-based responses"""
    
    def __init__(self, bot):
        self.bot = bot
        self.responses = {}  # {guild_id: [{trigger, response, embed_color}]}
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Check for auto-response triggers"""
        if message.author == self.bot.user or message.author.bot:
            return
        
        if message.guild.id not in self.responses:
            return
        
        for response_data in self.responses[message.guild.id]:
            trigger = response_data['trigger'].lower()
            
            # Check if trigger is in message
            if trigger in message.content.lower():
                response_text = response_data['response']
                embed_color = response_data.get('embed_color', 0x58A5FC)
                
                # Create response embed
                embed = discord.Embed(
                    title="🤖 Auto Response",
                    description=response_text,
                    color=discord.Color.from_rgb(
                        (embed_color >> 16) & 255,
                        (embed_color >> 8) & 255,
                        embed_color & 255
                    )
                )
                embed.set_footer(text=f"Trigger: {response_data['trigger']}")
                
                try:
                    await message.reply(embed=embed, mention_author=False)
                except discord.Forbidden:
                    pass
                
                # Only respond to first trigger
                break
    
    @commands.group(name='autoresponse', invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    async def autoresponse(self, ctx):
        """Auto-responder management commands"""
        embed = discord.Embed(
            title="🤖 Auto-Responder System",
            description="Automatic responses for common keywords",
            color=discord.Color.blue()
        )
        embed.add_field(name="`!autoresponse add <trigger> <response>`", value="Add auto-response", inline=False)
        embed.add_field(name="`!autoresponse remove <trigger>`", value="Remove auto-response", inline=False)
        embed.add_field(name="`!autoresponse list`", value="List all responses", inline=False)
        embed.add_field(name="`!autoresponse clear`", value="Clear all responses", inline=False)
        embed.set_footer(text="TableMC Development • Auto-Responder", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
        
        await ctx.send(embed=embed)
    
    @autoresponse.command(name='add')
    async def add_response(self, ctx, trigger: str, *, response: str):
        """Add an auto-response"""
        if ctx.guild.id not in self.responses:
            self.responses[ctx.guild.id] = []
        
        # Check if trigger already exists
        for data in self.responses[ctx.guild.id]:
            if data['trigger'].lower() == trigger.lower():
                embed = discord.Embed(
                    title="❌ Error",
                    description=f"Auto-response for '{trigger}' already exists!",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
        
        # Add new response
        self.responses[ctx.guild.id].append({
            'trigger': trigger,
            'response': response,
            'embed_color': 0x58A5FC,
            'created_by': ctx.author.id,
            'created_at': datetime.now()
        })
        
        embed = discord.Embed(
            title="✅ Auto-Response Added",
            color=discord.Color.green()
        )
        embed.add_field(name="Trigger", value=f"`{trigger}`", inline=True)
        embed.add_field(name="Response", value=f"```{response}```", inline=False)
        embed.add_field(name="Created By", value=ctx.author.mention, inline=True)
        embed.set_footer(text="Auto-Responder System")
        
        await ctx.send(embed=embed)
    
    @autoresponse.command(name='remove')
    async def remove_response(self, ctx, *, trigger: str):
        """Remove an auto-response"""
        if ctx.guild.id not in self.responses:
            embed = discord.Embed(
                title="❌ Error",
                description="No auto-responses configured",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        # Find and remove response
        for i, data in enumerate(self.responses[ctx.guild.id]):
            if data['trigger'].lower() == trigger.lower():
                removed = self.responses[ctx.guild.id].pop(i)
                
                embed = discord.Embed(
                    title="✅ Auto-Response Removed",
                    color=discord.Color.green()
                )
                embed.add_field(name="Trigger", value=f"`{removed['trigger']}`", inline=True)
                embed.add_field(name="Response", value=f"```{removed['response']}```", inline=False)
                
                await ctx.send(embed=embed)
                return
        
        embed = discord.Embed(
            title="❌ Error",
            description=f"Auto-response for '{trigger}' not found",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    
    @autoresponse.command(name='list')
    async def list_responses(self, ctx):
        """List all auto-responses"""
        if ctx.guild.id not in self.responses or len(self.responses[ctx.guild.id]) == 0:
            embed = discord.Embed(
                title="📋 Auto-Responses",
                description="No auto-responses configured",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(
            title="📋 Auto-Responses",
            description=f"Total: {len(self.responses[ctx.guild.id])}",
            color=discord.Color.blue()
        )
        
        for i, data in enumerate(self.responses[ctx.guild.id], 1):
            embed.add_field(
                name=f"{i}. {data['trigger']}",
                value=f"```{data['response']}```",
                inline=False
            )
        
        embed.set_footer(text="Use !autoresponse remove <trigger> to delete", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
        
        await ctx.send(embed=embed)
    
    @autoresponse.command(name='clear')
    async def clear_responses(self, ctx):
        """Clear all auto-responses"""
        if ctx.guild.id not in self.responses:
            embed = discord.Embed(
                title="❌ Error",
                description="No auto-responses to clear",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        count = len(self.responses[ctx.guild.id])
        self.responses[ctx.guild.id] = []
        
        embed = discord.Embed(
            title="✅ All Auto-Responses Cleared",
            description=f"Removed {count} auto-response(s)",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @autoresponse.command(name='edit')
    async def edit_response(self, ctx, trigger: str, *, new_response: str):
        """Edit an existing auto-response"""
        if ctx.guild.id not in self.responses:
            embed = discord.Embed(
                title="❌ Error",
                description="No auto-responses configured",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        for data in self.responses[ctx.guild.id]:
            if data['trigger'].lower() == trigger.lower():
                old_response = data['response']
                data['response'] = new_response
                data['updated_by'] = ctx.author.id
                data['updated_at'] = datetime.now()
                
                embed = discord.Embed(
                    title="✅ Auto-Response Updated",
                    color=discord.Color.green()
                )
                embed.add_field(name="Trigger", value=f"`{trigger}`", inline=True)
                embed.add_field(name="Old Response", value=f"```{old_response}```", inline=False)
                embed.add_field(name="New Response", value=f"```{new_response}```", inline=False)
                
                await ctx.send(embed=embed)
                return
        
        embed = discord.Embed(
            title="❌ Error",
            description=f"Auto-response for '{trigger}' not found",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    
    @autoresponse.command(name='search')
    async def search_responses(self, ctx, *, keyword: str):
        """Search auto-responses"""
        if ctx.guild.id not in self.responses:
            embed = discord.Embed(
                title="❌ Error",
                description="No auto-responses configured",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        results = [data for data in self.responses[ctx.guild.id] if keyword.lower() in data['trigger'].lower() or keyword.lower() in data['response'].lower()]
        
        if not results:
            embed = discord.Embed(
                title="❌ No Results",
                description=f"No auto-responses found matching '{keyword}'",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(
            title="🔍 Search Results",
            description=f"Found {len(results)} result(s)",
            color=discord.Color.blue()
        )
        
        for data in results:
            embed.add_field(
                name=data['trigger'],
                value=f"```{data['response']}```",
                inline=False
            )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AutoResponder(bot))
