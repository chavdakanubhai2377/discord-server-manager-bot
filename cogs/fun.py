import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    """Fun commands for entertainment"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='8ball', help='Ask the magic 8 ball')
    async def eight_ball(self, ctx, *, question):
        """Ask the magic 8 ball a question"""
        responses = [
            "Yes", "No", "Maybe", "Definitely", "Probably not",
            "Ask again later", "Absolutely", "Don't count on it",
            "Outlook good", "Very doubtful", "Signs point to yes"
        ]
        
        response = random.choice(responses)
        
        embed = discord.Embed(
            title='🎱 Magic 8 Ball',
            description=f'**Question:** {question}\n**Answer:** {response}',
            color=discord.Color.purple()
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='coinflip', help='Flip a coin')
    async def coinflip(self, ctx):
        """Flip a coin"""
        result = random.choice(['Heads', 'Tails'])
        
        embed = discord.Embed(
            title='🪙 Coin Flip',
            description=f'Result: **{result}**',
            color=discord.Color.gold()
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='roll', help='Roll a dice')
    async def roll(self, ctx, sides: int = 6):
        """Roll a dice"""
        if sides < 2:
            await ctx.send('❌ Dice must have at least 2 sides!')
            return
        
        result = random.randint(1, sides)
        
        embed = discord.Embed(
            title='🎲 Dice Roll',
            description=f'You rolled a **{result}** out of {sides}',
            color=discord.Color.green()
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='joke', help='Tell a joke')
    async def joke(self, ctx):
        """Tell a random joke"""
        jokes = [
            ("Why don't scientists trust atoms?", "Because they make up everything!"),
            ("What do you call a bear with no teeth?", "A gummy bear!"),
            ("Why did the scarecrow win an award?", "Because he was outstanding in his field!"),
            ("What's the best thing about Switzerland?", "I don't know, but their flag is a big plus!"),
            ("Why don't eggs tell jokes?", "They'd crack each other up!"),
        ]
        
        joke_setup, joke_punchline = random.choice(jokes)
        
        embed = discord.Embed(
            title='😂 Joke',
            description=f'**{joke_setup}**\n\n||{joke_punchline}||',
            color=discord.Color.blue()
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='rps', help='Play rock paper scissors')
    async def rock_paper_scissors(self, ctx, choice: str):
        """Play rock paper scissors with the bot"""
        choices = ['rock', 'paper', 'scissors']
        choice = choice.lower()
        
        if choice not in choices:
            await ctx.send('❌ Please choose: rock, paper, or scissors')
            return
        
        bot_choice = random.choice(choices)
        
        # Determine winner
        if choice == bot_choice:
            result = "It's a tie!"
            color = discord.Color.yellow()
        elif (choice == 'rock' and bot_choice == 'scissors') or \
             (choice == 'paper' and bot_choice == 'rock') or \
             (choice == 'scissors' and bot_choice == 'paper'):
            result = "You won! 🎉"
            color = discord.Color.green()
        else:
            result = "I won! 🤖"
            color = discord.Color.red()
        
        embed = discord.Embed(
            title='🎮 Rock Paper Scissors',
            color=color
        )
        embed.add_field(name='Your Choice', value=choice.capitalize(), inline=True)
        embed.add_field(name='My Choice', value=bot_choice.capitalize(), inline=True)
        embed.add_field(name='Result', value=result, inline=False)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))
