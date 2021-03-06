import argparse
import os
import pyperclip
import re
import requests
import shutil
import webbrowser

# register for client ID on twitch website and put here
TWITCH_CLIENT_ID = ''


class GetUrlAction(argparse.Action):
    """Argparse action to retrieve URL from the clipboard if none is
    provided by the user.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        # when no value is provided, it defaults to 'clip'
        # indicating we should grab url from the clipboard.
        if values is 'clip':
            values = pyperclip.paste()
        setattr(namespace, self.dest, values)


def out(str):
    """Print messages to standard output with twytch application prefix"""

    print("<-twytch-> {}".format(str))


def check_twitch_url(url):
    """Check the URL provided by the user is for Twitch.tv"""

    # this regex isn't perfect but it does the job
    return re.match('^(https?://)?(www\.)?twitch\.tv/\S*$', url)


def invalid_url(url):
    """Inform the user that an invalid URL was provided"""

    out("Invalid url: {}".format(url))


def query_api(query):
    """Make a request to the twitch api with the specified query.
    The query should not include the base API url as this is
    provided by the function itself.

    Keyword arguments:
    query -- The endpoint to query. eg: 'games/top'
    """

    headers = {'Client-ID': TWITCH_CLIENT_ID}

    uri = "https://api.twitch.tv/kraken/{}".format(query)
    response = requests.get(uri, headers=headers)
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        out("Error contacting twitch api, server returned: {}"
            .format(response.status_code))


def list_games():
    """Query the twitch API for the top games by number of viewers."""

    query = "games/top"
    top_games = query_api(query)
    games = []
    for key, item in enumerate(top_games["top"]):
        name = item["game"]["name"]
        out("{}: {} - {} viewers".format(key, name, item["viewers"]))
        games.append(name)
    choice = input("Pick a number: ")
    return games[int(choice)]


def list_top_streams_for_game(game, count=25):
    """List the top streams for the specified game.

    Keyword arguments:
    game -- the name of the game for which streams should be retrieved
    count -- the number of streams to get (default 25)
    """

    query = "streams?game={}&limit={}".format(game, count)
    channels = query_api(query)

    urls = []
    for key, item in enumerate(channels["streams"]):
        url = item["channel"]["url"]
        name = item["channel"]["display_name"]
        out("{}: {} - {}".format(str(key), name, url))
        urls.append(url)
    choice = input("Pick a number: ")
    url = urls[int(choice)]

    print(url)
    return url


def list_past_broadcasts(channel):
    """List available past broadcasts for the specified channel."""

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


def launch_stream(url, is_past_broadcast, perf_opts):
    """Launch the stream requested by the user

    Keyword arguments:
    url -- the URL of the stream to load
    is_past_broadcast -- whether to load as a past broadcast or not
    perf_opts --- a list of performance optimization options to pass to VLC
                  these will be in the following order:
                  file-caching (ms),
                  network-caching (ms),
                  hls-segment-threads (1-3).
                  Eg: [5000, 5000, 3]
    """

    perf_string = ' --player "vlc --file-caching {} ' \
                  '--network-caching {}" --hls-segment-threads {} '
    if shutil.which('livestreamer') is not None:
        out("livestreamer available, launching...")
        cmd_str = "livestreamer " + url + " source "
        if perf_opts is not None:
            cmd_str += perf_string.format(perf_opts[0],
                                          perf_opts[1],
                                          perf_opts[2])
        if is_past_broadcast:
            cmd_str += " --player-passthrough hls"

        cmd_str += ' --http-header Client-ID={}'.format(TWITCH_CLIENT_ID)
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
        nargs='?',
        const='25')

    perf_group = parser.add_mutually_exclusive_group()

    perf_group.add_argument(
        '-dperf',
        help='Add default performance optimizations to alleviate buffering.',
        action='store_true')

    perf_help_text = 'Specify performance optimzation parameters in this ' \
                     'order: file-caching (ms), network-caching (ms) and ' \
                     'hls-segment-threads (1-3). Eg: 5000 5000 3'

    perf_group.add_argument('-perf', help=perf_help_text, nargs=3, type=int)

    args = parser.parse_args()
    past_broadcast = False
    url = None

    if args.cs is not None:
        out("Loading top CS:GO streams")
        url = list_top_streams_for_game("Counter-Strike:+Global+Offensive", int(args.cs))
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

    perf_opts = None

    if url is not None:
        if args.dperf:
            # default values for performance optimizations
            perf_opts = [5000, 5000, 3]
        elif args.perf is not None:
            perf_opts = args.perf
        launch_stream(url, past_broadcast, perf_opts)
    else:
        out("No url :(")


if __name__ == '__main__':
    main()
