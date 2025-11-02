<div align="center">

# pdfdrive-api

**Unofficial Python wrapper for [pdfdrive.com.co](https://pdfdrive.com.co)**


[![PyPI version](https://badge.fury.io/py/pdfdrive-api.svg)](https://pypi.org/project/pdfdrive-api)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pdfdrive-api)](https://pypi.org/project/pdfdrive-api)
![Coverage](https://raw.githubusercontent.com/Simatwa/pdfdrive-api/refs/heads/main/assets/coverage.svg)
[![PyPI - License](https://img.shields.io/pypi/l/pdfdrive-api)](https://pypi.org/project/pdfdrive-api)
[![Downloads](https://pepy.tech/badge/pdfdrive-api)](https://pepy.tech/project/pdfdrive-api)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

</div>


##  Features

* Search ebooks with optional filters (tag, category, etc.)
* Explore books by categories or homepage
* Download ebooks asynchronously with high speed
* Full CLI support for interactive and automated usage
* Easy integration in scripts and applications


##  Installation

```bash
$ uv pip install "pdfdrive-api[cli]"
```

<details>

<summary>

## Developer Usage

</summary>

###  Download by URL

```python
from pdfdrive_api import BookDetails, Downloader

book_details = BookDetails(
    "https://pdfdrive.com.co/rich-dad-poor-dad-pdf/"
)

downloader = Downloader()

async def download_book():
    details = await book_details.get_details(for_download=True)
    download_url = details.book.download_url

    downloaded_file = await downloader.run(
        download_url,
        test=False,
        suppress_incompatible_error=True
    )

    print(downloaded_file)


if __name__ == "__main__":
    import asyncio
    asyncio.run(download_book())
```

---

###  Search and Download

```python
from pdfdrive_api import BookDetails, Downloader, SearchPage

async def main():
    search = SearchPage("Rich dad")
    resp = await search.get_content()
    target_book = resp.books.books[0]

    book_details = await BookDetails(target_book.url).get_details(for_download=True)
    downloader = Downloader()

    downloaded_file = await downloader.run(
        book_details.download_url,
        suppress_incompatible_error=True,
        test=True
    )

    print(downloaded_file)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

</details>

<details open>

<summary>

##  Command Line Interface (CLI)

</summary>

The package installs a CLI tool called `pdfdrive` for quick searching, exploring, and downloading ebooks.

```bash
pdfdrive --help
```

```
Usage: pdfdrive COMMAND

Explore, search and download ebooks from pdfdrive.com.co

Commands:
  download      Download ebook by specifying its title or page URL
  explore       Explore available ebooks by different criteria
  search        Search for a particular book by its title
  --help, -h    Display this message and exit
  --version, -v Display application version
```

---

###  `pdfdrive download`

```bash
pdfdrive download QUERY [ARGS]
```

Download an ebook by title or by its page URL.

| Parameter       | Aliases   | Description                                               | Default                      |
| --------------- | --------- | --------------------------------------------------------- | ---------------------------- |
| `QUERY`         | `--query` | Search text or book page URL.                             | **Required**                 |
| `--dir`         | `-d`      | Directory to save downloaded files.                       | `[current working directory]` |
| `--filename`    | `-f`      | Custom filename for output file.                          | Auto-generated               |
| `--connections` |           | Number of parallel download connections.                  | `5`                          |
| `--yes`, `-y`   |           | Proceed with the first search result automatically.       | `False`                      |
| `--quiet`, `-q` |           | Auto-download book whose title matches the query exactly. | `False`                      |

**Examples:**

```bash
# Download a book interactively
pdfdrive download "The Pragmatic Programmer"

# Auto-download first result
pdfdrive download "Clean Code" -y

# Download by URL
pdfdrive download "https://pdfdrive.com.co/book/clean-code-pdf/"

# Custom directory and filename
pdfdrive download "Deep Learning with Python" -d ~/Downloads -f deeplearning.pdf
```

###  `pdfdrive explore`

```bash
pdfdrive explore [ARGS]
```

Explore ebooks by category, tag, search query, or directly from a listing URL.

### Parameters

| Parameter                   | Aliases | Description                                | Default                                                                                                                                              |
| --------------------------- | ------- | ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--offset`                  | `-o`    | Page number to start from.                 | –                                                                                                                                                    |
| `--confirm`, `--no-confirm` | `-c`    | Ask before going to the next page.         | `False`                                                                                                                                               |
| `--details`, `--no-details` | `-d`    | Display detailed book info.                | `False`                                                                                                                                               |
| `--limit`                   | `-l`    | Number of pages to explore.                | `10`                                                                                                                                                 |
| `--infinity`                | `-i`    | Explore indefinitely without page limit.   | `False`                                                                                                                                              |
| `--search`                  | `-s`    | Explore by a text query.                   | –                                                                                                                                                    |
| `--category`                | `-c`    | Explore a category.                        | Choices include: `astrology`, `biography`, `academic-and-education`, `business-and-career`, `health`, `novels`, `self-improvement`, `religion`, etc. |
| `--name`                    | `-n`    | Explore books with a particular tag.       | –                                                                                                                                                    |
| `--url`                     | `-u`    | Explore books from a specific listing URL. | –                                                                                                                                                    |
| `--homepage`, `-home`       |         | Explore homepage content.                  | `True`                                                                                                                                               |

**Examples:**

```bash
# Explore homepage
pdfdrive explore

# Explore 5 pages in 'business-and-career' category
pdfdrive explore -c business-and-career -l 5

# Explore books tagged "machine learning"
pdfdrive explore -t "machine learning"

# Explore using URL
pdfdrive explore --u "https://pdfdrive.com.co/category/academic-and-education"

# Infinite exploration, auto-advance
pdfdrive explore -i
```

###  `pdfdrive search`

```bash
pdfdrive search QUERY [ARGS]
```

Search for a book by title. Optionally select, auto-proceed, or download directly.

| Parameter      | Aliases   | Description                                          | Default      |
| -------------- | --------- | ---------------------------------------------------- | ------------ |
| `QUERY`        | `--query` | Search text.                                         | **Required** |
| `--limit`      | `-l`      | Number of result pages to scan.                      | `1`          |
| `--yes`, `-y`  |           | Automatically select the first book found.           | `False`      |
| `--select-one` | `-s`      | Prompt user to select a book from results.           | Manual       |
| `--quiet`      | `-q`      | Automatically proceed if exact title match is found. | –            |

**Examples:**

```bash
# Search for a book interactively
pdfdrive search "Rich Dad Poor Dad"

# Auto-select first search result
pdfdrive search "Clean Architecture" -y

# Prompt to choose a book
pdfdrive search "Deep Learning" -s

# Quiet mode – exact title match
pdfdrive search "Atomic Habits" -q

# Search across 3 pages
pdfdrive search "Artificial Intelligence" -l 3
```

###  Summary

| Command             | Description                               |
| ------------------- | ----------------------------------------- |
| `pdfdrive download` | Download an ebook by title or URL         |
| `pdfdrive explore`  | Explore ebooks by category, tag, or query |
| `pdfdrive search`   | Search for a particular book by title     |

</details>