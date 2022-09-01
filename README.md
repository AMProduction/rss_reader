# RSS reader

RSS reader is a command-line utility which receives [RSS](https://en.wikipedia.org/wiki/RSS) URL and prints results in
human-readable format.

## How to use

### Usage

```
usage: RSS reader [-h] [--url URL] [--version] [-j] [--verbose] [--limit LIMIT] [--date DATE] [--to_pdf] [--to_html]

Pure Python command-line RSS reader.

options:
  -h, --help     show this help message and exit
  --url URL      RSS feed URL
  --version      Print version info and exits
  -j, --json     Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided
  --date DATE    The date getting news from local storage
  --to_pdf       Save results as PDF file
  --to_html      Save results as HTML file

Enjoy the program!
```

### Install dependencies

If you are using Linux OS:

```
pip install -r requirements.txt
```

If you are using Windows OS:

```
python -m pip install -r requirements.txt
```

### How to run

```
python rss_reader.py --url https://news.yahoo.com/rss/ --limit 3 --verbose --json --date 20220830 --to_pdf --to_html
```

### How to run tests

```
python -m unittest discover -v
```

#### Coverage

1. Install coverage.py:

    ```
    pip install coverage
    ```

2. Use `coverage run` to run your test suite and gather data:
    
    ```
    coverage run -m unittest discover
    ```

3. Use `coverage report` to report on the results:
    ```
    coverage report -m
    ```
4. For a nicer presentation, use `coverage html` to get annotated HTML listings detailing missed lines:
    ```
    coverage html
    ```
   Then open `tests/coverage/index.html` in your browser, to see a report

5. To exclude tests from the coverage report:

    ```
    coverage html --omit="*/test*" -d tests/coverage
    ```

