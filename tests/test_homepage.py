import pytest

from pdfdrive_api.core.finder.extractor import PageListingExtractor
from pdfdrive_api.core.finder.models import ContentPageModel
from pdfdrive_api.main import Homepage
from tests import index_path_content

extractor = PageListingExtractor(index_path_content)

# TODO: Add tests for other extractor methods


def test_book_listing_extraction():
    page_content = extractor.extract_page_content()

    assert isinstance(page_content, ContentPageModel)


@pytest.mark.asyncio
async def test_homepage():
    homepage = Homepage()
    contents = await homepage.get_content()

    assert isinstance(contents, ContentPageModel)

    next_page = await homepage.next_page(contents)
    assert isinstance(next_page, Homepage)

    next_contents = await next_page.get_content()

    assert isinstance(next_contents, ContentPageModel)

    previous_page = await next_page.previous_page(next_contents)

    assert isinstance(previous_page, Homepage)

    previous_contents = await previous_page.get_content()

    assert isinstance(previous_contents, ContentPageModel)
