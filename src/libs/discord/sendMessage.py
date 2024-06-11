async def sendMessage(bot, channel_id, message):
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)
    else:
        print(f"Could not find channel with ID {channel_id}")
