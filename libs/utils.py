import aiohttp
import asyncio
import json
from json import load
from dotenv import load_dotenv
import os


def loadf(filename):
    with open(filename, "r", encoding='utf-8') as f:
        return load(f)


def writef(data: object, filename: object) -> object:
    with open(filename, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def env(key):
    load_dotenv()
    result = os.getenv(key)
    return result


def check_if_admin(ctx):
    config = loadf('./config.json')
    admin_users = config['administrative_users']
    return ctx.message.author.id in admin_users


async def get_user_info(discord_id):
    async with aiohttp.ClientSession() as session:
        dashactyl_token = env('DASHACTYL_TOKEN')
        Headers = {
            'Authorization': f'Bearer {dashactyl_token}'}
        Data = {'id': str(discord_id)}
        async with session.get(url='https://cp.cygennodes.com/api/userinfo', headers=Headers, params=Data) as resp:
            return await resp.json()


async def set_coins(discord_id, coins):
    dashactyl_token = env('DASHACTYL_TOKEN')
    Headers = {'Authorization': f'Bearer {dashactyl_token}'}
    Data = {'id': str(discord_id), 'coins': int(coins)}
    async with aiohttp.ClientSession() as session:
        async with session.post(url='https://cp.cygennodes.com/api/setcoins', headers=Headers, json=Data) as resp:
            return resp.status


async def create_ptero_server(name, user_id, allocation_id, type_server):
    global data
    ptero_token = env('PTERO_TOKEN')
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ptero_token}',
    }
    if type_server == 1:
        data = {"name": name, "user": int(user_id), "egg": 3, "docker_image": "ghcr.io/pterodactyl/yolks:java_16",
                "startup": "java -Xms128M -Xmx{{SERVER_MEMORY}}M -jar {{SERVER_JARFILE}}",
                "environment": {"MINECRAFT_VERSION": "latest", "SERVER_JARFILE": "server.jar", "BUILD_NUMBER": "latest",
                                "DL_PATH": ""},
                "limits": {"memory": 1024, "swap": 128, "disk": 2048, "io": 500, "cpu": 50},
                "feature_limits": {"databases": 0, "backups": 1}, "allocation": {"default": int(allocation_id)}}
    elif type_server == 2:
        data = {"name": name, "user": int(user_id), "egg": 5, "docker_image": "ghcr.io/pterodactyl/yolks:java_16",
                "startup": "java -Xms128M -Xmx{{SERVER_MEMORY}}M -jar {{SERVER_JARFILE}}",
                "environment": {"SERVER_JARFILE": "server.jar", "VANILLA_VERSION": "latest"},
                "limits": {"memory": 1024, "swap": 128, "disk": 2048, "io": 500, "cpu": 50},
                "feature_limits": {"databases": 0, "backups": 1}, "allocation": {"default": int(allocation_id)}}
    elif type_server == 4:
        data = {"name": name, "user": int(user_id), "egg": 1, "docker_image": "ghcr.io/pterodactyl/yolks:java_8",
                "startup": "java -Xms128M -Xmx{{SERVER_MEMORY}}M -jar {{SERVER_JARFILE}}",
                "environment": {"BUNGEE_VERSION": "latest", "SERVER_JARFILE": "bungeecord.jar"},
                "limits": {"memory": 1024, "swap": 128, "disk": 2048, "io": 500, "cpu": 50},
                "feature_limits": {"databases": 0, "backups": 1}, "allocation": {"default": int(allocation_id)}}
    elif type_server == 3:
        data = {"name": name, "user": int(user_id), "egg": 2, "docker_image": "ghcr.io/pterodactyl/yolks:java_16",
                "startup": "java -Xms128M -Xmx{{SERVER_MEMORY}}M -jar {{SERVER_JARFILE}}",
                "environment": {"SERVER_JARFILE": "server.jar", "MC_VERSION": "latest", "BUILD_TYPE": "recommended",
                                "FORGE_VERSION": ""},
                "limits": {"memory": 1024, "swap": 128, "disk": 2048, "io": 500, "cpu": 50},
                "feature_limits": {"databases": 0, "backups": 1}, "allocation": {"default": int(allocation_id)}}
    elif type_server == 5:
        data = {"name": name, "user": int(user_id), "egg": 17,
                "docker_image": "quay.io/parkervcp/pterodactyl-images:base_debian",
                "startup": "./bin/php7/bin/php ./PocketMine-MP.phar --no-wizard --disable-ansi",
                "environment": {"VERSION": "latest", "GITHUB_PACKAGE": "pmmp/PocketMine-MP",
                                "MATCH": "PocketMine-MP.phar"},
                "limits": {"memory": 1024, "swap": 128, "disk": 2048, "io": 500, "cpu": 50},
                "feature_limits": {"databases": 0, "backups": 1}, "allocation": {"default": int(allocation_id)}}
    elif type_server == 6:
        data = {"name": name, "user": int(user_id), "egg": 18,
                "docker_image": "quay.io/parkervcp/pterodactyl-images:base_debian",
                "startup": "./bedrock_server",
                "environment": {"BEDROCK_VERSION": "latest", "LD_LIBRARY_PATH": ".",
                                "SERVERNAME": "Bedrock Dedicated Server",
                                "GAMEMODE": "survival", "DIFFICULTY": "easy", "CHEATS": "false"},
                "limits": {"memory": 1024, "swap": 128, "disk": 2048, "io": 500, "cpu": 50},
                "feature_limits": {"databases": 0, "backups": 1}, "allocation": {"default": int(allocation_id)}}

    async with aiohttp.ClientSession() as session:
        async with session.post('https://gp.cygennodes.com/api/application/servers', headers=headers,
                                json=data) as resp:
            return resp.status


async def get_allocation_id():
    ptero_token = env('PTERO_TOKEN')
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ptero_token}'}
    forever_variable = True
    request_url = 'https://gp.cygennodes.com/api/application/nodes/1/allocations'
    while forever_variable:
        async with aiohttp.ClientSession() as session:
            async with session.get(request_url, headers=headers) as resp:
                response = await resp.json()

        # Checks only the allocation value
        input_json = response['data']
        # Checks only the allocations are not assigned
        filtered_list = [obj for obj in input_json if (obj['attributes']['assigned'] is False)]

        # checks if there is any unused allocations in the current page, if not it goes to a new page
        if len(filtered_list) != 0:
            allocation_id = filtered_list[1]
            return allocation_id['attributes']['id']
        else:
            # Tries to find a new page to send a request to, if not then all allocations are declared as full
            try:
                request_url = response['meta']['pagination']['links']['next']
            except Exception as e:
                print(e)
                return 'Allocations are full. Please try again later'
