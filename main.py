import chess
import discord
from discord.ext import commands

from config import TOKEN

bot = commands.Bot(command_prefix='&')

isBoard = False
game = []

@bot.command()
async def start(ctx):
    global board
    global isBoard # using global variables is probably not 
                   # a good idea but what i have to say is

    isBoard = True 
    board = chess.Board()

    await ctx.channel.send("Board was created.")


@bot.command()
async def move(ctx, arg):
    global isBoard
    global game

    if isBoard: 
        try:
            board.push_san(arg)

        except ValueError:
            await ctx.channel.send("Invalid move.")
            return

        if board.is_game_over():
            await ctx.channel.send(board.outcome(claim_draw=True))
            await end(ctx)

        elif board.is_check():
            await ctx.channel.send("Check.")
        else:
            await ctx.message.add_reaction("✅")

        game.append(arg)

    else:
        await ctx.channel.send("Board wasn't created. Use &start to create.")


@bot.command()
async def log(ctx):
    global game

    if len(game) == 0:
        await ctx.channel.send("No piece was moved yet.")
        return

    result = ""

    n = 1
    for i in range(len(game)):
        if i % 2: 
            result += " " + game[i] + "\n"
        else:
            result += str(n) + ". " + game[i]

        n += 1

    await ctx.channel.send("```" + str(result) + "```")
    

@bot.command()
async def end(ctx):
    global board
    global game

    await ctx.channel.send("```" + str(board) + "```")
    await ctx.channel.send("Game ended. Board is reset.")
    
    game = [] 
    board.reset()


bot.run(TOKEN)
