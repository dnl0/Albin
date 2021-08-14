import chess
import end
import move
import discord
import json
from main import isBoard
from discord.ext import commands

class StartCog(commands.Cog, name="start"):
    def __init__(self, bot:commands.Bot):
		    self.bot = bot

    @commands.command(name = "start",
                    usage="start",
                    description = "start chessing")
    @commands.cooldown(1, 2, commands.BucketType.member)

    async def start(ctx):
        global board
        global isBoard # using global variables is probably not 
                    # a good idea but what i have to say is

        isBoard = True 
        board = chess.Board()

        await ctx.channel.send("Board was created.")

def setup(bot:commands.Bot): 
	bot.add_cog(StartCog(bot)) 