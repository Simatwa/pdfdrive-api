import pytest

from pdfdrive_api.download import Downloader
from pdfdrive_api.extras import BookDetails, BookPageModel
from pdfdrive_api.requests import Session

link = "https://pdfdrive.com.co/rich-dad-poor-dad-pdf/"


@pytest.mark.asyncio
async def test_book_details_extraction():
    book_details = BookDetails(link, session=Session())
    details = await book_details.get_details(for_download=True)
    assert isinstance(details, BookPageModel)


@pytest.mark.asyncio
async def test_book_download():
    book_details = BookDetails(link, session=Session())
    downloader = Downloader()

    details = await book_details.get_details(for_download=True)
    download_url = details.book.download_url

    resp = await downloader.run(
        download_url, test=True, suppress_incompatible_error=True
    )
    assert resp.is_success
