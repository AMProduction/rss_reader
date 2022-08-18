# RSS reader

RSS reader is a command-line utility which receives [RSS](https://en.wikipedia.org/wiki/RSS) URL and prints results in
human-readable format.

## How to use

### Usage

```
usage: RSS reader [-h] [--version] [-j] [--verbose] [--limit LIMIT] url

Pure Python command-line RSS reader.

positional arguments:
  url            RSS feed URL

options:
  -h, --help     show this help message and exit
  --version      Print version info and exits
  -j, --json     Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided

Enjoy the program!
```

### Install dependencies

If you are using Linux OS:

```
$ pip install -r requirements.txt
```

If you are using Windows OS:

```
python -m pip install -r requirements.txt
```

### How to run

```
python rss_reader.py "https://news.yahoo.com/rss/" --limit -3 --verbose --json
```

### How to run autotests

```
$ python -m unittest discover
```

