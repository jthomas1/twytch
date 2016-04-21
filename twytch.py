import os
import sys
import requests
import getopt
import shutil
import webbrowser


def usage():
    help_text = """
        Usage:
            -u or --url followed by a valid twitch url for livestream
            -p or --past followed by a valid twitch past broadcast url
            --csgo for a list of top csgo streams
    """
    print(help_text)

try:
    short_opts = "u:p:h"
    long_opts = ["url=", "csgo", "help"]
    opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    api_url = "https://api.twitch.tv/kraken/streams?game="
    past_broadcast = False
    for o, a in opts:
        if o in ("-u", "--url"):
            address = a
        elif o in ("-p", "--past"):
            address = a
            past_broadcast = True
        elif o == "--csgo":
            url = api_url + "Counter-Strike:+Global+Offensive"
            response = requests.get(url)
            if response.status_code == requests.codes.ok:
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
        cmd_str = "livestreamer " + address + " source "
        if(past_broadcast):
            cmd_str += " --player-passthrough hls"
        os.system(cmd_str)
    else:
        print("livestreamer unavailable, falling back to browser")
        webbrowser.open(address)


except getopt.GetoptError as err:
    print(err)
    usage()
    sys.exit(2)
