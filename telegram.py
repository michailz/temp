import asyncio
import configparser
import hashlib
import os
import json
import sys
from pathlib import Path
from telethon.tl.types import PeerUser, PeerChat, PeerChannel, InputChannel
from telethon import TelegramClient, utils, types
from telethon.tl.functions.channels import GetFullChannelRequest, GetChannelsRequest
from datetime import date, datetime


config = configparser.ConfigParser()
config_path = Path(__file__).parent.resolve()
config.read(os.path.join(config_path, "config.ini"))
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']
phone_number = config['Telegram']['phone']
client = TelegramClient(username, int(api_id), api_hash)


async def main():
    # Create the client and connect
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start(phone_number)

    # Get all dialogs (conversations/chats)
    dialogs = await client.get_dialogs()

    # Filter dialogs to only channels
    channels = [dialog.entity for dialog in dialogs if dialog.is_channel]

    # Prepare the list of InputChannels for GetChannelsRequest
    input_channels = [InputChannel(channel.id, channel.access_hash) for channel in channels]

    # Fetch full channel details
    if input_channels:
        result = await client(GetChannelsRequest(input_channels))
        channel_details = {channel.id: channel for channel in result.chats}

        # Dump messages for each channel
        for channel in channels:
            messages = []
            async for message in client.iter_messages(channel, min_id=0, reverse=True):
                messages.append(json.loads(message.to_json()))

            # Save messages to a JSON file named after the channel ID
            with open(f'{channel.id}.json', 'w', encoding='utf-8') as f:
                json.dump(messages, f, ensure_ascii=False, indent=4)

    # Disconnect the client
    await client.disconnect()

# Run the main function
if __name__ == '__main__':
    asyncio.run(main())




