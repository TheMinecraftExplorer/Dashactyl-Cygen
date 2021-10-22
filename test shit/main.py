import requests


def check_coins(discord_id):
    Headers = {'Authorization': 'Bearer KoWJWr&dw3xpRZAhHt#ztjUrno7Yau#L^E$b5yM*K$^8F!8D6s@J8RJ4KNRDRoYcu!Ed@paw'}
    Data = {'id': str(discord_id)}
    r = requests.post('https://dashactyl.beap.xyz/api/userinfo', headers=Headers, params=Data)
    response = r.json()
    coins = int(response['coins'])


def set_coins(discord_id, coins):
    Headers = {'Authorization': 'Bearer KoWJWr&dw3xpRZAhHt#ztjUrno7Yau#L^E$b5yM*K$^8F!8D6s@J8RJ4KNRDRoYcu!Ed@paw'}
    Data = {'id': str(discord_id), 'coins': int(coins)}
    r = requests.get('https://dashactyl.beap.xyz/api/userinfo', headers=Headers, params=Data)
    response = r.json()
    coins = int(response['coins'])
    return coins


user_coins = check_coins('707549304382029845')


if user_coins is not None:
    if user_coins >= 500:
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer afsrzAADvXLZQxoKlY7R4UeB5XTJSrNjsoJPCl2yWlTJRE8l',
        }

        data = '{ "name": "Building", "user": 1, "egg": 1, "docker_image": "quay.io/pterodactyl/core:java", "startup": "java -Xms128M -Xmx128M -jar server.jar", "environment": { "BUNGEE_VERSION": "latest", "SERVER_JARFILE": "server.jar" }, "limits": { "memory": 128, "swap": 0, "disk": 512, "io": 500, "cpu": 100 }, "feature_limits": { "databases": 5, "backups": 1 }, "allocation": { "default": 17 } }'

        response = requests.post('https://gp.beap.xyz/api/application/servers', headers=headers, data=data)
