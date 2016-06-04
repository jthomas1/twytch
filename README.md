# twytch
A simple python command line interface for accessing Twitch.tv live streams and past broadcasts using [Livestreamer](http://docs.livestreamer.io/) for an enhanced viewing experience.

If you do not have Livestreamer available your default web browser will be used as a fallback.

## Usage
All Urls must be valid for twitch.tv eg: https://twitch.tv/mychannel

### Positional arguments:
- [Url] If nothing is specified clipboard content is used.

### Optional arguments:
- [-p] Same as Url except for past broadcasts.
- [-pb] List past broadcasts for a specified channel name.
- [-cs] Choose from a list of the top 25 CS:GO live streams

### Examples:
- `python twytch.py https://twitch.tv/mychannel` loads the steam at "channel"
- `python twytch.py` - loads a stream url which has been copied to the clipboard.
- `python twytch.py -p https://twitch.tv/mychannel/v/123456` loads the past broadcast specified
- `python twytch.py -p` loads the past broadcast from a url on the clipboard
- `python twytch.py -pb mychannel` lists the past broadcasts for "mychannel"
- `python twytch,.py -cs` lists top 25 live streams for CS:GO 
