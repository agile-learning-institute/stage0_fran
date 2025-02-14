import discord
import ollama
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Create bot instance
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        print("Echo, echo, echo")
        return
    
    ctype = message.channel.type
    print(f"Channel Type: {ctype} is {type(ctype)}")
    if message.channel.type != discord.ChannelType.private and message.channel.name not in ["fran","workshop"]:
        print(f"Just snooping on {message.channel}")
        return
    
    guild = message.guild
    user_name = message.author
    user_message = message.content
    channel = message.channel

    channel_id = channel.id
    channel_name = "DM"
    channel_category = "Direct"
    if channel.type != discord.ChannelType.private:
        channel_name = channel.name
        channel_category = channel.category
    
    response = ollama.chat(model='llama3.2:latest', messages=[
        {
            'role': 'user',
            'content': user_message,
        },
    ])
    print(f"Guild {guild}, Category {channel_category}, Channel {channel_name}-{channel_id}, user {user_name}, message {user_message}, ollama says {response}")
    await message.channel.send(f"Hello {user_name} from {guild} on {channel} in {channel_category} - Ollama says: {response.message.content}")

# Run bot
client.run(TOKEN)
