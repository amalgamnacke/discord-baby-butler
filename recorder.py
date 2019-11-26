import discord
from discord.ext import commands
from discord import VoiceChannel
from foobardb import FoobarDB

class Recorder(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None
		self.db = FoobarDB("./data.db")

	@commands.Cog.listener()
	async def on_ready(self):
		print("Joining voice channel")

		channel = await self.bot.fetch_channel("636151702218735650")
		self.vc = await channel.connect()
		#vc = VoiceChannel(name="General")
		#vc.connect()
		#channel = self.bot.get_channel("636151702218735650")
		#channel.connect()

	@commands.command(name="commands", aliases=["c"])
	async def show_commands(self, ctx, *, member: discord.Member = None):
		await ctx.send("```!hello - bot says hello```")

	@commands.command()
	async def p(self, ctx, *, channel: discord.VoiceChannel = None):
		# loop attachments .a
		print("Source object {0}".format(self.vc))
		#return await ctx.send("Source)

	@commands.command(name="parsehistory", aliases=["ph"])
	async def parse_history(self, ctx, *, channel: discord.TextChannel = None):
		for guild in self.bot.guilds:
			for channel in guild.text_channels:
				print("Processing {}.".format(channel.name))

				async for message in channel.history(limit=None):
					self.store_attachments(message)

	def is_image_extension(self, filename):
		return filename.endswith(("jpg", "png", "jpeg", "bmp", "gif"))

	def store_attachments(self, message):
		if message.type != discord.MessageType.default:
			print("not default message type {}".format(message.type))
			return

		for attachment in message.attachments:
			#check for youtube etc
			if not self.is_image_extension(attachment.filename):
				print("is not image {}".format(attachment.filename))
				continue

			print("Storing new attachment message for url'{0}'.".format(attachment.url))
			self.db.set(message.id, {"id": message.id, "message": message.content, "author": message.author.display_name, "jump_url": message.jump_url, "attachments": [{"id": attachment.id, "url": attachment.url}]})

	def delete_all_attachments(self, message):
		if message.type != discord.MessageType.default:
			return

		self.db.delete(message.id)

	@commands.Cog.listener()
	async def on_message(self, message):
		print("on message")
		self.store_attachments(message)

	@commands.Cog.listener()
	async def on_message_delete(self, message):
		print("on delete")
		self.delete_all_attachments(message)

	@commands.Cog.listener()
	async def on_bulk_message_delete(self, messages):
		print("on bulk delete")
		for message in messages:
			self.delete_all_attachments(message)

	@commands.Cog.listener()
	async def on_message_edit(self, before, after):
		print("on edit")
		self.delete_all_attachments(before)
		self.store_attachments(after)

	@commands.command()
	async def join(self, ctx, *, channel: discord.VoiceChannel = None):
		if ctx.voice_client is not None:
			return await ctx.voice_client.move_to(channel)

		await channel.connect()

	@commands.command()
	async def hello(self, ctx, *, member: discord.Member = None):
		"""Says hello"""
		member = member or ctx.author

		if self._last_member is None or self._last_member.id != member.id:
			await ctx.send("Hello {0.name}~".format(member))
		else:
			await ctx.send("Hello {0.name}...this feels samiliar.".format(member))

		self._last_member = member

	@commands.Cog.listener()
	async def on_member_join(self, member):
		channel = member.guild.system_channel

		if channel is not None:
			await channel.send("Welcome {0.mention}.".format(member))

	@commands.Cog.listener()
	async def on_group_join(self, channel, user):
		await channel.send("qwe")
		print("User {0.name} joined channel {1.name}.".format(user, channel))

	@commands.Cog.listener()
	async def on_group_remove(self, channel, user):
		await channel.send("asd")
		print("User {0.name} left channel {1.name}.".format(user, channel))
