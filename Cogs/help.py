import discord
from discord.ext import commands

class HelpCog(commands.Cog, name="help commmand"):
    def __init__(self, bot:commands.Bot):
		    self.bot = bot

    @commands.command(name = "help",
                    usage="help",
                    description = "displays help command")
    @commands.cooldown(1, 2, commands.BucketType.member)

    async def help(self, ctx:commands.Context):
          await ctx.send("bla bla bla help command bla bla bla")
          print("Help command sent!")

def setup(bot:commands.Bot): 
	bot.add_cog(HelpCog(bot)) 