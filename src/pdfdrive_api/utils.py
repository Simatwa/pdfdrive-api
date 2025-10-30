from bs4 import BeautifulSoup as bts
from pdfdrive_api.types import Html, HtmlSoup


def souper(content: Html | HtmlSoup) -> HtmlSoup:
    if isinstance(content, HtmlSoup):
        return content

    soup = bts(content, "html.parser")
    return soup
