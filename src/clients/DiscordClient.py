import discord
import asyncio
import utils.index as utils
from constants import CONSTANTS
from clients.TweepyClient import TweepyClient

class DiscordClient(discord.Client):
    def __init__(self, * args, ** kwargs):
        super().__init__( * args, ** kwargs)
        self.guild_id = CONSTANTS['guild_id']

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        stream = TweepyClient(CONSTANTS['Consumer_Key'], CONSTANTS['Consumer_Secret'], CONSTANTS['Access_Key'], CONSTANTS['Access_Secret'], loop=asyncio.get_event_loop(), send_to_channel=self.send_to_channel)
        stream.filter(track=["@blaccxyz_", "#BlackTechTwitter"], filter_level='low', threaded=True)

    async def send_to_channel(self, tweetData):
        guild = self.get_guild(self.guild_id)
        channel_id = await utils.get_channel_id(guild, tweetData[0])

        if channel_id is None:
            return

        channel = guild.get_channel(channel_id)

        if channel is None:
            return

        await channel.send("https://twitter.com/twitter/statuses/" + str(tweetData[1]))



