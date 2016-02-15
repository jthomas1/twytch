import os
import sys
import pyperclip
import requests


if len(sys.argv) > 1:
    address = ' '.join(sys.argv[1:])
else:
    address = pyperclip.paste()

url = "https://api.twitch.tv/kraken/streams?game=Counter-Strike:+Global+Offensive"

response = requests.get(url)

if(response.status_code == 200):
    channels = response.json()
    urls = []
    for item in channels["streams"]:
        urls.append(item["channel"]["url"])
    os.system("livestreamer " + urls[0] + " source")
else:
    print("No response")