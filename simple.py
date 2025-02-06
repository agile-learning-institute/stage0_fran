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
    
    if message.channel.name not in ["fran","workshop-be1df368-9169-442e-8f63-0bc4a5df7b54"]:
        print(f"Just snooping on {message.channel}")
        return
    
    user_name = message.author
    user_message = message.content
    channel = message.channel
    category = channel.category
    guild = message.guild
    
    response = ollama.chat(model='llama3.2:latest', messages=[
        {
            'role': 'user',
            'content': user_message,
        },
    ])
    print(f"Guild {guild}, Category {category}, Channel {channel}, user {user_name}, message {user_message}, ollama says {response}")
    await message.channel.send(f"Hello {user_name} from {guild} on {channel} in {category} - Ollama says: {response.message.content}")

# Run bot
client.run(TOKEN)
