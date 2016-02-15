import os
import sys
import requests


if len(sys.argv) > 1:
    address = ' '.join(sys.argv[1:])
else:
    url = "https://api.twitch.tv/kraken/streams?game=Counter-Strike:+Global+Offensive&limit=1"
    response = requests.get(url)

    if(response.status_code == 200):
        channels = response.json()
        for item in channels["streams"]:
            address = item["channel"]["url"]

os.system("livestreamer " + address + " source")
