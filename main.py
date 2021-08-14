import chess
import discord
import json
from discord.ext import commands

with open("configuration.json", "r") as config: 
	data = json.load(config)
	token = data["token"]
	prefix = data["prefix"]
        
intents = discord.Intents.all()

bot = commands.Bot(prefix, case_insensitive = True, intents = intents)
bot.remove_command("help")

initial_extensions = [
	"Cogs.help",
]

print(initial_extensions)

if __name__ == '__main__':
	for extension in initial_extensions:
		try:
			bot.load_extension(extension)
			print(f"Extensions loaded: {extension}")
		except Exception as e:
			print(f"Failed to load extension {extension}.")

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("chessing"))
    print("")
    print(f"Logged in as {bot.user}")

isBoard = False

# @bot.command()
# async def start(ctx):
#     global board
#     global isBoard # using global variables is probably not 
#                    # a good idea but what i have to say is

#     isBoard = True 
#     board = chess.Board()

#     await ctx.channel.send("Board was created.")


# @bot.command()
# async def move(ctx, arg):
#     global isBoard

#     if isBoard: 
#         try:
#             board.push_san(arg)

#             if board.is_game_over():
#                 await ctx.channel.send(board.outcome(claim_draw=True))
#                 await end(ctx)

#             elif board.is_check():
#                 await ctx.channel.send("Check.")
#             else:
#                 await ctx.message.add_reaction("✅")

#         except ValueError:
#             await ctx.channel.send("Invalid move.")
#     else:
#         await ctx.channel.send("Board wasn't created. Use &start to create.")


# @bot.command()
# async def end(ctx):
#     global board

#     await ctx.channel.send("```" + str(board) + "```")
#     await ctx.channel.send("Game ended. Board is reset.")
    
#     board.reset()


bot.run(token)
