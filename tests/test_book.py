from pdfdrive_api.core.book.extractor import BookDetailsExtractor
from pdfdrive_api.core.book.models import (
    BookPageModel,
)
from tests import book_path_content

extractor = BookDetailsExtractor(book_path_content)


# TODO: Add tests for other methods


def test_page_content_extraction():
    page_content = extractor.extract_page_content()
    assert isinstance(page_content, BookPageModel)
