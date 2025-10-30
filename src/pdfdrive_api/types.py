import typing as t

from bs4 import BeautifulSoup

Html = t.TypeVar("Html", bound=str)

HtmlSoup = t.TypeVar("HtmlSoup", bound=BeautifulSoup)
