import discord
from discord.ext import commands
import jishaku # For debugging
import data # Take the token that stored in data.py


# Definite the BOT
intents = discord.Intents.default()
intents.members = True 
activity = discord.Activity(type=discord.ActivityType.watching, name="for chat | $help") # You can change this status into yours
bot = commands.Bot(command_prefix="$", intents=intents,activity=activity)
# command_prefix="$" can be changed into anything you want

# These are the cogs
bot.load_extension('jishaku')
bot.load_extension("basic")
bot.load_extension('moderation')
bot.load_extension('fun')
bot.load_extension('pokemon')
bot.load_extension('server')



@bot.event
async def on_ready():
	print('Connected to bot: {}'.format(bot.user.name))
	print('Bot ID: {}'.format(bot.user.id))



# This will change the status of the BOT
@bot.command(description="*For owner only*: Change Articuno's status")
@commands.is_owner()
async def change(ctx, type, *, status):
	if type.startswith("play"):
		await bot.change_presence(activity=discord.Game(name=status))
	if type.startswith("watch"):
		await bot.change_presence(activity=discord.Activity(
		    type=discord.ActivityType.watching, name=status))
	if type.startswith("stream"):
		await bot.change_presence(activity=discord.Activity(
		    type=discord.ActivityType.streaming, name=status))
	if type.startswith("listen"):
		await bot.change_presence(activity=discord.Activity(
		    type=discord.ActivityType.listening, name=status))
	await ctx.send("BOT's status changed successfully")




# Put your token here
bot.run(data.TOKEN)
