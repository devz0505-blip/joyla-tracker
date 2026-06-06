import requests
import json
import os

WEBHOOK = "https://discord.com/api/webhooks/1511520864674517032/8DDozcoAmyzQqO5fZMpYgGzUG8Dfwj_NJr5z0heCumgbq_3IhMQRT972VexXi7kDXmu2"

ARTIST_ID = "2tgbyi1wLVMKi75RXukSTQ"

CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]

def get_token():
    r = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(CLIENT_ID, CLIENT_SECRET)
    )
    return r.json()["access_token"]

token = get_token()

headers = {
    "Authorization": f"Bearer {token}"
}

r = requests.get(
    f"https://api.spotify.com/v1/artists/{ARTIST_ID}/albums?include_groups=single,album",
    headers=headers
)

latest = r.json()["items"][0]

release_id = latest["id"]

try:
    with open("last_release.txt", "r") as f:
        last_id = f.read().strip()
except:
    last_id = ""

if release_id == last_id:
    print("Schon gepostet")
    exit()

name = latest["name"]
url = latest["external_urls"]["spotify"]

requests.post(
    WEBHOOK,
    json={
        "content": f"🎵 Neuer Release von Joyla!\n\n{name}\n{url}"
    }
)

with open("last_release.txt", "w") as f:
    f.write(release_id)
