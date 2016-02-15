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
        for key, item in enumerate(channels["streams"]):
            url = item["channel"]["url"]
            print(str(key) + ": " + url)
            urls.append(url)
        choice = input("Pick a number: ")
        address = urls[int(choice)]

os.system("livestreamer " + address + " source")
