import os
import sys
import requests
import getopt

try:
    opts, args = getopt.getopt(sys.argv[1:], "u:h", ["url=", "csgo", "help"])
    api_url = "https://api.twitch.tv/kraken/streams?game="

    for o, a in opts:
        if o in ("-u", "--url"):
            address = a
        elif o == "--csgo":
            url = api_url + "Counter-Strike:+Global+Offensive"
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
        elif o in ("-h", "--help"):
            # usage()
            sys.exit()

        os.system("livestreamer " + address + " source")

except getopt.GetoptError as err:
    # print help information and exit:
    print(err)
    # usage()
    sys.exit(2)
