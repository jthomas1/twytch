import os
import sys
import requests


if len(sys.argv) > 1:
    address = ' '.join(sys.argv[1:])
else:
    url = "https://api.twitch.tv/kraken/streams?game=Counter-Strike:+Global+Offensive"
    response = requests.get(url)

    if(response.status_code == 200):
        channels = response.json()
        urls = []
        for item in channels["streams"]:
          urls.append(item["channel"]["url"])
        address  = urls[0]

os.system("livestreamer " + address + " source")
