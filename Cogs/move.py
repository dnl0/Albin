import end
import start
import chess
import discord
import json
from discord.ext import commands
from start import *

isBoard = False

class MoveCog(commands.Cog, name="move"):
    def __init__(self, bot:commands.Bot):
		    self.bot = bot

    @commands.command(name = "move",
                    usage="move",
                    description = "move a piece")
    @commands.cooldown(1, 2, commands.BucketType.member)


    async def move(ctx, arg):
        global isBoard

        if isBoard: 
            try:
                board.push_san(arg)

                if board.is_game_over():
                    await ctx.channel.send(board.outcome(claim_draw=True))
                    await end(ctx)

                elif board.is_check():
                    await ctx.channel.send("Check.")
                else:
                    await ctx.message.add_reaction("✅")

            except ValueError:
                await ctx.channel.send("Invalid move.")
        else:
            await ctx.channel.send("Board wasn't created. Use &start to create.")

def setup(bot:commands.Bot): 
	bot.add_cog(MoveCog(bot)) 