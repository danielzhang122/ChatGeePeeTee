import discord
from discord.ext import commands
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# -------- CONFIG --------
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# -------- EVENTS --------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    # Ignore the bot itself
    if message.author == bot.user:
        return

    # Check if bot is mentioned
    if bot.user in message.mentions:
        user_message = message.content.replace(f"<@{bot.user.id}>", "").strip()

        if user_message == "":
            await message.channel.send("Say something after pinging me.")
            return

        # Call ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful Discord bot."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response["choices"][0]["message"]["content"]
        await message.channel.send(reply)

    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
