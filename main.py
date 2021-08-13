import chess
import discord
from discord.ext import commands

from config import TOKEN

isBoard = False

bot = commands.Bot(command_prefix='&')

@bot.command()
async def start(ctx):
    global board
    global isBoard # using global variables is probably not 
                   # a good idea but what i have to say is

    isBoard = True 
    board = chess.Board()

    await ctx.channel.send("Board was created.")


@bot.command(pass_context=True)
async def move(ctx, arg):
    global isBoard

    if isBoard: 
        try:
            board.push_san(arg)

            # game ends
            if board.is_checkmate():
                await ctx.channel.send("Checkmate.")
            elif board.is_stalemate():
                await ctx.channel.send("Stalemate.")
            elif board.is_insufficient_material():
                await ctx.channel.send("Insufficient material.")
            elif board.is_repetition():
                await ctx.channel.send("Repetition of moves.")

            # other cases
            elif board.is_check():
                await ctx.channel.send("Check.")
                return

            else:
                return
            
            await end(ctx)
            
        except ValueError:
            await ctx.channel.send("Invalid move.")
    else:
        await ctx.channel.send("Board wasn't created. Use &start to create.")


@bot.command()
async def end(ctx):
    global board

    await ctx.channel.send("```" + str(board) + "```")
    await ctx.channel.send("Game ended. Board is cleared.")
    
    board = chess.Board()


bot.run(TOKEN)
