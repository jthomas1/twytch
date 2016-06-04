# twytch
A simple python command line interface for accessing Twitch.tv live streams and past broadcasts using [Livestreamer](http://docs.livestreamer.io/) for an enhanced viewing experience.

If you do not have Livestreamer available your default web browser will be used as a fallback.

## Usage
All Urls must be valid for twitch.tv eg: https://twitch.tv/mychannel

### Positional arguments:
- [Url] If nothing is specified clipboard content is used.

### Optional arguments:
- [-p] Same as Url except for past broadcasts.
- [-g] List the top 10 games and then use that choice to list top 25 streams for that game.
- [-pb] List past broadcasts for a specified channel name.
- [-cs] Choose from a list of the top 25 CS:GO live streams.

### Examples:
```
# Loads the steam at "channel"
$ python twytch.py https://twitch.tv/mychannel 
```

```
# Loads a stream url which has been copied to the clipboard.
$ python twytch.py
```

```
# Loads the past broadcast specified
$ python twytch.py -p https://twitch.tv/mychannel/v/123456
```

```
# Loads the past broadcast from a url on the clipboard
$ python twytch.py -p
```

```
# Loads a list of the top 10 games
$ python twytch.py -g
```

```
# Lists the past broadcasts for "mychannel"
$ python twytch.py -pb mychannel
```

```
# Lists top 25 live streams for CS:GO 
$ python twytch,.py -cs
```
