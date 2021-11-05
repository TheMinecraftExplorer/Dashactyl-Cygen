import discord
import asyncio
from discord.ext import commands
import platform
import os
from libs.utils import env, loadf

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='.', intents=intents, case_insensitive=True)

client.config = loadf('./config.json')


async def status_task():
    while True:
        activity = discord.Activity(name=f"Welcome to Cygen", type=discord.ActivityType.watching)
        await client.change_presence(status=discord.Status.idle, activity=activity)
        await asyncio.sleep(20)
        activity2 = discord.Activity(name=f".help | {len(set(client.users))} users", type=discord.ActivityType.playing)
        await client.change_presence(status=
                                     discord.Status.idle, activity=activity2)
        activity3 = discord.Activity(name=".create_server <name> to create a server in Singapore",
                                     type=discord.ActivityType.playing)
        await client.change_presence(status=discord.Status.idle, activity=activity3)
        activity4 = discord.Activity(name=f"You need {client.config['server_price']} coins to create a server.",
                                     type=discord.ActivityType.playing)
        await client.change_presence(status=discord.Status.idle, activity=activity4)
        await asyncio.sleep(20)


@client.event
async def on_ready():
    print("-------------------")
    print(f"Logged in as {client.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print(f"Bot by TME#7107")
    print("-------------------")
    client.load_extension('cogs.servers')
    client.loop.create_task(status_task())


client.run(env('DISCORD_TOKEN'))