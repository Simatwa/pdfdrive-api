import pytest

from pdfdrive_api.download import Downloader
from pdfdrive_api.extras import BookDetails, BookPageModel

book_details = BookDetails("https://pdfdrive.com.co/rich-dad-poor-dad-pdf/")
downloader = Downloader()


@pytest.mark.asyncio
async def test_book_details_extraction():
    details = await book_details.get_details()
    assert isinstance(details, BookPageModel)


@pytest.mark.asyncio
async def test_book_download():
    details = await book_details.get_details()
    download_url = details.book.download_url

    resp = await downloader.run(download_url, test=True)
    assert resp.is_success
