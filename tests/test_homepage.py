from pdfdrive_api.core.finder.extractor import PageListingExtractor
from pdfdrive_api.core.finder.models import ContentPageModel
from tests import index_path_content

extractor = PageListingExtractor(
    index_path_content
)

# TODO: Add tests for other extractor methods


def test_book_listing_extraction():
    page_content = extractor.extract_page_content()

    assert isinstance(page_content, ContentPageModel)