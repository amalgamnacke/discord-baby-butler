import configparser

import discord
import logging
from discord.ext import commands
from recorder import Recorder

config = configparser.ConfigParser()
config.read("config.ini")
config = config["settings"]

# Config logging.
logging.basicConfig(level=logging.INFO)
#discord.opus.load_opus("opus")
print(discord.opus.is_loaded())

class ButlerBot(discord.ext.commands.Bot):
	async def on_ready(self):
		self.print_on_ready_info()

		#print(self.cogs["recorder"])

	def print_on_ready_info(self):
		print("------")
		print("discord.py version {0}.".format(discord.__version__))
		print("Logged in as {0} ({0.id}).".format(self.user))
		print("------")

		#print("Joining first voice channel.")
		#print(vars(bot.voice_clients))

# Start the bot.
botClient = ButlerBot(command_prefix="!")
botClient.add_cog(Recorder(botClient))
print(config)
botClient.run(config["token"])
#botClient.run('MzY1NTE5OTEyMTMyOTM1Njk0.XdfSKA.4k_hQwId3i3gl3EvYOaYVOV8CKU')

#@bot.command()
#async def ping(ctx):
#    await ctx.send('pong')

# Attach cogs.
#bot.add_cog(Recorder(bot))

# Start bot.
#bot.run('MzY1NTE5OTEyMTMyOTM1Njk0.XdfSKA.4k_hQwId3i3gl3EvYOaYVOV8CKU')
