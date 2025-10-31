import pytest

from pdfdrive_api.download import Downloader
from pdfdrive_api.extras import BookDetails, BookPageModel

book_details = BookDetails("https://pdfdrive.com.co/rich-dad-poor-dad-pdf/")
downloader = Downloader()


@pytest.mark.asyncio
async def test_book_details_extraction():
    details = await book_details.get_details(for_download=True)
    assert isinstance(details, BookPageModel)


@pytest.mark.asyncio
async def test_book_download():
    details = await book_details.get_details(for_download=True)
    download_url = details.book.download_url

    resp = await downloader.run(download_url, test=True, suppress_incompatible_error=True)
    assert resp.is_success
