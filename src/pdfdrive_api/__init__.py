# TODO: Complete this
""" """

from importlib import metadata

try:
    __version__ = metadata.version("pdfdrive-api")
except metadata.PackageNotFoundError:
    __version__ = "0.0.0"

__author__ = "Smartwa"
__repo__ = "https://github.com/Simatwa/pdfdrive-api"


from pdfdrive_api.core.book.extractor import BookDetailsExtractor
from pdfdrive_api.core.book.models import BookPageModel
from pdfdrive_api.core.finder.extractor import PageListingExtractor
from pdfdrive_api.core.finder.models import ContentPageModel
from pdfdrive_api.download import Downloader
from pdfdrive_api.extras import BookDetails, Extras
from pdfdrive_api.pages import (
    BookPage,
    CategoryPage,
    HomePage,
    SearchPage,
    TagPage,
    URLPage,
)

__all__ = [
    "BookDetailsExtractor",
    "BookPageModel",
    "PageListingExtractor",
    "ContentPageModel",
    "Downloader",
    "BookDetails",
    "Extras",
    "BookPage",
    "CategoryPage",
    "HomePage",
    "SearchPage",
    "TagPage",
    "URLPage",
]
