import requests

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer afsrzAADvXLZQxoKlY7R4UeB5XTJSrNjsoJPCl2yWlTJRE8l',
}

data = '{ "name": "Building", "user": 1, "egg": 1, "docker_image": "quay.io/pterodactyl/core:java", "startup": "java -Xms128M -Xmx128M -jar server.jar", "environment": { "BUNGEE_VERSION": "latest", "SERVER_JARFILE": "server.jar" }, "limits": { "memory": 128, "swap": 0, "disk": 512, "io": 500, "cpu": 100 }, "feature_limits": { "databases": 5, "backups": 1 }, "allocation": { "default": 17 } }'

response = requests.post('https://gp.beap.xyz/api/application/servers', headers=headers, data=data)
print(response)
