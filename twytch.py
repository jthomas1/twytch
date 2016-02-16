import os
import sys
import requests
import getopt
import shutil
import webbrowser


def usage():
    help_text = """
        Usage:
            -u or --url followed by a valid twitch url
            --csgo for a list of top csgo streams
    """
    print(help_text)

try:
    short_opts = "u:h"
    long_opts = ["url=", "csgo", "help"]
    opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    api_url = "https://api.twitch.tv/kraken/streams?game="
    for o, a in opts:
        if o in ("-u", "--url"):
            address = a
        elif o == "--csgo":
            url = api_url + "Counter-Strike:+Global+Offensive"
            response = requests.get(url)
            if(response.status_code == requests.codes.ok):
                channels = response.json()
                urls = []
                for key, item in enumerate(channels["streams"]):
                    url = item["channel"]["url"]
                    name = item["channel"]["display_name"]
                    print("{}: {} - {}".format(str(key), name, url))
                    urls.append(url)
                choice = input("Pick a number: ")
                address = urls[int(choice)]
        elif o in ("-h", "--help"):
            usage()
            sys.exit()

    if shutil.which('livestreamer') is not None:
        print("livestreamer available, launching...")
        os.system("livestreamer " + address + " source")
    else:
        print("livestreamer unavailable, falling back to browser")
        webbrowser.open(address)


except getopt.GetoptError as err:
    print(err)
    usage()
    sys.exit(2)
