from bs4 import BeautifulSoup as bts

from pdfdrive_api.types import Html, HtmlSoup


def souper(content: Html | HtmlSoup) -> bts:
    if isinstance(content, bts):
        return content

    soup = bts(content, "html.parser")
    return soup


def slugify(tag: str) -> str:
    return tag.lower().replace(" ", "-")
