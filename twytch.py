import os
import argparse
import requests
import shutil
import webbrowser
import pyperclip


class GetUrlAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values is 'clip':
            values = pyperclip.paste()
        setattr(namespace, self.dest, values)


def out(str):
    print("<-twytch-> {}".format(str))


def check_twitch_url(url):
    if "twitch.tv/" in url:
        return True
    else:
        return False


def invalid_url(url):
    out("Invalid url: {}".format(url))


def get_top_streams():
    csgo_uri = "https://api.twitch.tv/kraken/streams?game=" \
               "Counter-Strike:+Global+Offensive"
    response = requests.get(csgo_uri)
    if response.status_code == requests.codes.ok:
        channels = response.json()
        urls = []
        for key, item in enumerate(channels["streams"]):
            url = item["channel"]["url"]
            name = item["channel"]["display_name"]
            out("{}: {} - {}".format(str(key), name, url))
            urls.append(url)
        choice = input("Pick a number: ")
        return urls[int(choice)]


def launch_stream(url, is_past_broadcast):
    if shutil.which('livestreamer') is not None:
        out("livestreamer available, launching...")
        cmd_str = "livestreamer " + url + " source "
        if(is_past_broadcast):
            cmd_str += " --player-passthrough hls"
        os.system(cmd_str)
    else:
        out("livestreamer unavailable, falling back to browser")
        webbrowser.open(url)


def main():
    parser = argparse.ArgumentParser(
        description='Description of your program')
    parser.add_argument(
        'url',
        help='Load twitch live stream by URL',
        type=str,
        const="clip",
        action=GetUrlAction,
        nargs='?')
    parser.add_argument(
        '-p',
        help='Load twitch past broadcast by URL',
        type=str,
        const="clip",
        action=GetUrlAction,
        nargs='?')
    parser.add_argument(
        '-cs',
        help='Show list of top CS:GO stream',
        action="store_true")

    args = parser.parse_args()
    past_broadcast = False
    url = None

    if args.cs is True:
        out("Loading top CS:GO streams")
        get_top_streams()
    elif args.p is not None:
        out("Loading past broadcast")
        if check_twitch_url(args.p):
            url = args.p
            past_broadcast = True
        else:
            invalid_url(args.p)
    elif args.url is not None:
        out("Loading live stream")
        if check_twitch_url(args.url):
            url = args.url
        else:
            invalid_url(args.url)
    else:
        out("Something went wrong :(")

    if url is not None:
        launch_stream(url, past_broadcast)
    else:
        out("No url :(")


if __name__ == '__main__':
    main()
