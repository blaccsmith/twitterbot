import discord
from os import environ

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.guild_messages = True

CONSTANTS = {
    'Consumer_Key' : environ['Consumer_Key'],
    'Consumer_Secret' : environ['Consumer_Secret'],
    'Access_Key' : environ['Access_Key'],
    'Access_Secret' : environ['Access_Secret'],
    'moderator_id' : environ['moderator_id'],
    "Discord_Token": environ['Discord_Token'],
    'guild_id' : environ['guild_id'],
    'intents': intents
}

