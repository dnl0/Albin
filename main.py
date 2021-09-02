import chess
import random
import chess.engine
import discord
from discord.ext import commands

from config import TOKEN

bot = commands.Bot(command_prefix="&")

isBoard = False
game = []


@bot.command()
async def start(ctx, user: discord.Member = None, variation: str = None):
    global board
    global botIsPlayer
    global isBoard
    global white_id
    global black_id

    botIsPlayer = False

    bot_id = await bot.application_info()
    if not user:
        await ctx.channel.send("Tag a user to play.")
        return

    elif user.id == bot_id.id:
        botIsPlayer = True

    white_id = ctx.author.id
    black_id = user.id

    isBoard = True

    if not variation:
        board = chess.Board()
    elif variation == "960" or variation == "chess960":
        r = random.randint(0, 959)
        board = chess.Board().from_chess960_pos(r)
        await ctx.channel.send(str(board))
    else:
        await ctx.channel.send("Unknown chess variant.")
        return

    await ctx.channel.send("Board was created.")
    await ctx.channel.send(f"White: {ctx.message.author.mention}\nBlack: {user.mention}")


@start.error
async def start_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.channel.send("User not found.")


@bot.command()
async def move(ctx, arg):
    if isBoard:
        try:
            author_id = ctx.author.id

            if board.turn and author_id == white_id:  # board.turn returns True if
                # white to move and false otherwise
                pass
            elif not board.turn and author_id == black_id:
                pass
            else:
                await ctx.channel.send("You can't move for other player.")
                return

            board.push_san(arg)

        except ValueError:
            await ctx.channel.send("Invalid move.")
            return

        if board.is_game_over():
            s = str(board.outcome(claim_draw=True).termination)
            s = s.split(".")
            await ctx.channel.send(s[-1])
            await end(ctx)

        elif board.is_check():
            await ctx.channel.send("Check.")
        else:
            await ctx.message.add_reaction("✅")

        game.append(arg)

        if botIsPlayer:
            engine = chess.engine.SimpleEngine.popen_uci("stockfish")
            # 0.1 because maybe the player will have a tiny chance, if stockfish doesn't do the *perfect* moves
            limit = chess.engine.Limit(time=0.1)
            move = engine.play(board, limit)
            if move.move is None:
                if move.resigned:
                    await ctx.channel.send("Engine resigned; Congratulations!")
                    await end(ctx)
                    return

                elif move.draw_offered:
                    await ctx.channel.send("Engine offered you a draw, do you accept? (This isn't implemented yet :/)")
                    await end(ctx)
                    return

            move_normal_notation = board.san(move.move)
            await ctx.channel.send(move_normal_notation)
            board.push(move.move)
            game.append(move_normal_notation)

            if board.is_game_over():
                await ctx.channel.send(board.outcome(claim_draw=True))
                await end(ctx)
            elif board.is_check():
                await ctx.channel.send("Check.")

    else:
        await ctx.channel.send("Board wasn't created. Use &start to create.")


@bot.command()
async def log(ctx):
    if len(game) == 0:
        await ctx.channel.send("No piece was moved yet.")
        return

    result = ""

    n = 1
    for i in range(len(game)):
        if i % 2:
            result += " " + game[i] + "\n"
            continue
        else:
            result += str(n) + ". " + game[i]

        n += 1

    await ctx.channel.send("```" + str(result) + "```")


@bot.command()
async def end(ctx):
    global board
    global game
    global botIsPlayer

    await ctx.channel.send("```" + str(board) + "```")
    await ctx.channel.send("Game ended. Board is reset.")

    game = []
    board.reset()
    botIsPlayer = False


bot.run(TOKEN)
