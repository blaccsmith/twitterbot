async def get_channel_id(guild, tweet_text):
    fetched_channels = await guild.fetch_channels()
    for channel in fetched_channels:
        if channel.name in tweet_text:
            return channel.id
    return None