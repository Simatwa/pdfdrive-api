<div align="center">

# pdfdrive-api

**Unofficial Python wrapper for pdfdrive.com.co** - Explore, search and download ebooks from pdfdrive.com.co

[![PyPI version](https://badge.fury.io/py/pdfdrive-api.svg)](https://pypi.org/project/pdfdrive-api)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pdfdrive-api)](https://pypi.org/project/pdfdrive-api)
![Coverage](https://raw.githubusercontent.com/Simatwa/pdfdrive-api/refs/heads/main/assets/coverage.svg)
[![PyPI - License](https://img.shields.io/pypi/l/pdfdrive-api)](https://pypi.org/project/pdfdrive-api)
[![Downloads](https://pepy.tech/badge/pdfdrive-api)](https://pepy.tech/project/pdfdrive-api)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

</div>

# Features

- Search ebooks with optional filters ie. Tag, Category etc
- Faster download speed
- Fully asynchronous

# Installation

```sh
$ uv pip install pdfdrive-api
```

# Usage 


## Download by url

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

    print(
        downloaded_file
    )


if __name__ == "__main__":

    import asyncio
    asyncio.run(download_book())
```

## Search and download


```python

from pdfdrive_api import BookDetails, Downloader, SearchPage


async def main():
    search = SearchPage("Rich dad")

    resp = await search.get_content()
    target_book = resp.books.books[0]

    book_details = await BookDetails(target_book.url).get_details(
        for_download=True
    )

    downloader = Downloader()

    downloaded_file = await downloader.run(
        book_details.download_url,
        suppress_incompatible_error=True,
        test=True
    )

    print(
        downloaded_file
    )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

> [!NOTE]
> There's more than just what you've gone through. Checkout later.