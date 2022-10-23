import asyncio
from constants import CONSTANTS
from clients.DiscordClient import DiscordClient

async def connect_client():
    client = DiscordClient(intents=CONSTANTS['intents'])
    await client.login(CONSTANTS['Discord_Token'])
    await client.connect()

def start():
    asyncio.run(connect_client())

if __name__ == '__main__':
    start()
