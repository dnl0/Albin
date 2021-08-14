import discord
import json
import move
import start
import chess
from start import *
from discord.ext import commands

class EndCog(commands.Cog, name="end"):
    def __init__(self, bot:commands.Bot):
		    self.bot = bot

    @commands.command(name = "end",
                    usage="end",
                    description = "end game")
    @commands.cooldown(1, 2, commands.BucketType.member)


    async def end(ctx):
        global board

        await ctx.channel.send("```" + str(board) + "```")
        await ctx.channel.send("Game ended. Board is reset.")
        
        board.reset()

def setup(bot:commands.Bot): 
	bot.add_cog(EndCog(bot)) 