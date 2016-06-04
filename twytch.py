import argparse
import os
import pyperclip
import re
import requests
import shutil
import webbrowser


class GetUrlAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # when no value is provided, it defaults to 'clip'
        # indicating we should grab url from the clipboard.
        if values is 'clip':
            values = pyperclip.paste()
        setattr(namespace, self.dest, values)


def out(str):
    print("<-twytch-> {}".format(str))


def check_twitch_url(url):
    # this regex isn't perfect but it does the job
    return re.match('^(https?://)?(www\.)?twitch\.tv/\S*$', url)


def invalid_url(url):
    out("Invalid url: {}".format(url))


def query_api(query):
    uri = "https://api.twitch.tv/kraken/{}".format(query)
    response = requests.get(uri)
    if response.status_code == requests.codes.ok:
        return response.json()


def list_games():
    query = "games/top"
    top_games = query_api(query)
    games = []
    for key, item in enumerate(top_games["top"]):
        name = item["game"]["name"]
        out("{}: {} - {} viewers".format(key, name, item["viewers"]))
        games.append(name)
    choice = input("Pick a number: ")
    return games[int(choice)]


def list_top_streams_for_game(game):
    query = "streams?game={}".format(game)
    channels = query_api(query)
    urls = []
    for key, item in enumerate(channels["streams"]):
        url = item["channel"]["url"]
        name = item["channel"]["display_name"]
        out("{}: {} - {}".format(str(key), name, url))
        urls.append(url)
    choice = input("Pick a number: ")
    return urls[int(choice)]


def list_past_broadcasts(channel):
    query = "channels/{}/videos?broadcasts=true".format(channel)
    json_data = query_api(query)
    urls = []
    for key, item in enumerate(json_data["videos"]):
        title = item["title"]
        url = item["url"]
        out("{}: {} - {}".format(str(key), title, url))
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
        description='Simple twitch.tv stream loader.')
    parser.add_argument(
        'url',
        help='Load live stream by URL specified as parameter or from the clipboard',
        type=str,
        const="clip",
        action=GetUrlAction,
        nargs='?')
    parser.add_argument(
        '-p',
        help='Load a past broadcast by URL specified as parameter or from the clipboard.',
        type=str,
        const="clip",
        action=GetUrlAction,
        nargs='?')
    parser.add_argument(
        '-g',
        help='List streams by choosing a game.',
        action="store_true")
    parser.add_argument(
        '-pb',
        help='List past broadcasts for a particular channel.',
        type=str)
    parser.add_argument(
        '-cs',
        help='List top CS:GO streams.',
        action="store_true")

    args = parser.parse_args()
    past_broadcast = False
    url = None

    if args.cs is True:
        out("Loading top CS:GO streams")
        url = list_top_streams_for_game("Counter-Strike:+Global+Offensive")
    elif args.g is True:
        out("Loading games")
        game = list_games()
        out("Loading top streams for {}".format(game))
        url = list_top_streams_for_game(game.replace(" ", "+"))
    elif args.pb is not None:
        past_broadcast = True
        url = list_past_broadcasts(args.pb)
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
