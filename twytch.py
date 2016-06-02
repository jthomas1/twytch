import os
import sys
import argparse
import requests
import shutil
import webbrowser
import pyperclip


help_text = """
        Usage:
            -u followed by a valid twitch url for livestream
            -p followed by a valid twitch past broadcast url
            --csgo for a list of top csgo streams
    """

csgo_uri = "https://api.twitch.tv/kraken/streams?game=" \
           "Counter-Strike:+Global+Offensive"


def usage():
    print(help_text)


def check_twitch_url(url):
    if "twitch.tv/" in url:
        return True
    else:
        return False


def invalid_url(url):
    print("Invalid url: {}".format(url))


def get_top_streams():
    response = requests.get(csgo_uri)
    if response.status_code == requests.codes.ok:
        channels = response.json()
        urls = []
        for key, item in enumerate(channels["streams"]):
            url = item["channel"]["url"]
            name = item["channel"]["display_name"]
            print("{}: {} - {}".format(str(key), name, url))
            urls.append(url)
        choice = input("Pick a number: ")
        return urls[int(choice)]


def main():
    parser = argparse.ArgumentParser(
        description='Description of your program')
    parser.add_argument(
        'url',
        help='Load twitch live stream by URL',
        nargs='?')
    parser.add_argument(
        '-p',
        help='Load twitch past broadcast by URL',
        const="clip",
        nargs='?')

    args = parser.parse_args()
    print(args)

    past_broadcast = False

    if args.url is not None:
        # use livestream url provided
        if check_twitch_url(args.url):
            url = args.url
        else:
            invalid_url(args.url)
    elif args.url is None and args.p is None:
        # get live stream url from pyperclip
        if check_twitch_url(args.url):
            url = pyperclip.paste()
        else:
            invalid_url(args.url)
    elif args.url is None and args.p is "clip":
        # get live stream url from pyperclip
        if check_twitch_url(args.p):
            url = pyperclip.paste()
            past_broadcast = True
        else:
            invalid_url(args.p)
    elif args.p is not None:
        # use past broadcast url provided
        if check_twitch_url(args.p):
            url = args.p
            past_broadcast = True
        else:
            invalid_url(args.p)
    else:
        print(":(")

    if shutil.which('livestreamer') is not None:
        print("livestreamer available, launching...")
        cmd_str = "livestreamer " + url + " source "
        if(past_broadcast):
            cmd_str += " --player-passthrough hls"
        os.system(cmd_str)
    else:
        print("livestreamer unavailable, falling back to browser")
        webbrowser.open(url)


if __name__ == '__main__':
    main()
