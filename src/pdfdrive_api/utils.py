import re

from bs4 import BeautifulSoup as bts

from pdfdrive_api.constants import BASE_URL, BOOK_PAGE_URL_PATTERN
from pdfdrive_api.types import Html, HtmlSoup


def souper(content: Html | HtmlSoup) -> bts:
    if isinstance(content, bts):
        return content

    soup = bts(content, "html.parser")
    return soup


def slugify(tag: str) -> str:
    return tag.lower().replace(" ", "-")


def is_url(text: str) -> bool:
    test = re.match(r"^\w{2,6}://.+", text, re.IGNORECASE)
    return test is not None


def is_valid_url(url: str) -> bool:
    test = re.match(r"^" + BASE_URL, url, re.IGNORECASE)
    return test is not None


def validate_book_page_url(book_page_url: str) -> str:
    if not BOOK_PAGE_URL_PATTERN.match(book_page_url):
        raise ValueError(
            f"Invalid value for specific book page url - {book_page_url}"
        )
    return book_page_url


def remove_tags(html: str, replace_with: str = "") -> str:
    return re.sub(r"<[^>]*>", replace_with, html)


def remove_tag_attributes(html: str) -> str:
    return re.sub(r"<(\w+)(?:\s+[^>]*)?>", r"<\1>", html)
