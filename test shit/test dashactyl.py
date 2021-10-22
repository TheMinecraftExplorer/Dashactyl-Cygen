import requests


def set_coins(discord_id, coins):
    Headers = {'Authorization': 'Bearer KoWJWr&dw3xpRZAhHt#ztjUrno7Yau#L^E$b5yM*K$^8F!8D6s@J8RJ4KNRDRoYcu!Ed@paw'}
    Data = {'id': str(discord_id), 'coins': int(coins)}
    r = requests.post('https://dashactyl.beap.xyz/api/setcoins', headers=Headers, json=Data)
    return r.json()

Headers = {'Authorization': 'Bearer KoWJWr&dw3xpRZAhHt#ztjUrno7Yau#L^E$b5yM*K$^8F!8D6s@J8RJ4KNRDRoYcu!Ed@paw'}
Data = {'id': '768828430153940994'}
r = requests.get('https://dashactyl.beap.xyz/api/userinfo', headers=Headers, params=Data)
response = r.json()
print(response)
