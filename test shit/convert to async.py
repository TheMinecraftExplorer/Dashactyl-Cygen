import aiohttp
import asyncio


async def get_coins():
    async with aiohttp.ClientSession() as session:
        Headers = {'Authorization': 'Bearer KoWJWr&dw3xpRZAhHt#ztjUrno7Yau#L^E$b5yM*K$^8F!8D6s@J8RJ4KNRDRoYcu!Ed@paw'}
        Data = {'id': '707549304382029845'}
        async with session.get(url='https://dashactyl.beap.xyz/api/userinfo', headers=Headers, params=Data) as resp:
            print(await resp.json())


async def create_ptero_server(name):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer afsrzAADvXLZQxoKlY7R4UeB5XTJSrNjsoJPCl2yWlTJRE8l',
    }

    data = '{ "name": "Building", "user": 1, "egg": 1, "docker_image": "quay.io/pterodactyl/core:java", "startup": "java -Xms128M -Xmx128M -jar server.jar", "environment": { "BUNGEE_VERSION": "latest", "SERVER_JARFILE": "server.jar" }, "limits": { "memory": 128, "swap": 0, "disk": 512, "io": 500, "cpu": 100 }, "feature_limits": { "databases": 5, "backups": 1 }, "allocation": { "default": 17 } }'

    async with aiohttp.ClientSession() as session:
        async with session.post('https://gp.beap.xyz/api/application/servers', headers=headers, data=data) as resp:
            return resp.status


loop = asyncio.get_event_loop()
loop.run_until_complete(get_coins())
