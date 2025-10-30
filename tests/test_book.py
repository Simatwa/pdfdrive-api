from pdfdrive_api.core.book.extractor import BookDetailsExtractor
from pdfdrive_api.core.book.models import (
    BookPageModel,
    PageMetadataModel,
)
from tests import book_path_content

extractor = BookDetailsExtractor(
    book_path_content
)


def test_page_metadata_extraction():
    page_metadata = extractor.extract_page_metadata()
    assert isinstance(page_metadata, PageMetadataModel)


# TODO: Add tests for other methods


def test_page_content_extraction():
    page_content = extractor.extract_page_content()
    assert isinstance(page_content, BookPageModel)