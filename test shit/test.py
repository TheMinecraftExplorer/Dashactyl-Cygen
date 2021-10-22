import requests
import aiohttp
import json
from libs.utils import env

'''headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer afsrzAADvXLZQxoKlY7R4UeB5XTJSrNjsoJPCl2yWlTJRE8l',
}

data = '{ "name": "Building", "user": 1, "egg": 1, "docker_image": "quay.io/pterodactyl/core:java", "startup": "java -Xms128M -Xmx128M -jar server.jar", "environment": { "BUNGEE_VERSION": "latest", "SERVER_JARFILE": "server.jar" }, "limits": { "memory": 128, "swap": 0, "disk": 512, "io": 500, "cpu": 100 }, "feature_limits": { "databases": 5, "backups": 1 }, "allocation": { "default": 17 } }'

response = requests.post('https://gp.beap.xyz/api/application/servers', headers=headers, data=data)
print'''


def get_allocation_id():
    ptero_token = env('PTERO_TOKEN')
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ptero_token}'}
    forever_variable = True
    request_url = 'https://gp.cygennodes.com/api/application/nodes/4/allocations'
    while forever_variable:
        r = requests.get(request_url, headers=headers)
        response = r.json()

        input_json = response['data']
        filtered_list = [obj for obj in input_json if (obj['attributes']['assigned'] is False)]

        if len(filtered_list) != 0:
            allocation_id = filtered_list[1]
            return allocation_id['attributes']['id']
        else:
            try:
                request_url = response['meta']['pagination']['links']['next']
            except Exception as e:
                print(e)
                return 'Allocations are full. Please try again later'


print(get_allocation_id())

