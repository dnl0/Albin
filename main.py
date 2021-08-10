import chess
import discord
from discord.ext import commands
from config import TOKEN

isBoard = True 
board = chess.Board()

client = discord.Client()
bot = commands.Bot(command_prefix='&')

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))

@bot.command()
async def start(ctx):
    await ctx.channel.send("Board was created.")

@bot.command()
async def move(ctx, arg):
    if isBoard: 
        try:
            board.push_san(arg)
        except ValueError:
            await ctx.channel.send("Invalid move.")
            return
    else:
        await ctx.channel.send("Board wasn't created. Use &start to create.")
        return

@bot.command()
async def print(ctx):
    await ctx.channel.send("```" + str(board) + "```")


bot.run(TOKEN)
