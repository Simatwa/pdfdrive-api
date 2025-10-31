import pytest

from pdfdrive_api.constants import BooksCategory
from pdfdrive_api.core.finder.models import ContentPageModel
from pdfdrive_api.pages import CategoryPage


@pytest.mark.asyncio
async def test_category_page():
    search = CategoryPage(BooksCategory.ACADEMIC_AND_EDUCATION.value)
    contents = await search.get_content()

    assert isinstance(contents, ContentPageModel)

    next_page = await search.next_page(contents)
    assert isinstance(next_page, CategoryPage)

    next_contents = await next_page.get_content()

    assert isinstance(next_contents, ContentPageModel)

    previous_page = await next_page.previous_page(next_contents)

    assert isinstance(previous_page, CategoryPage)

    previous_contents = await previous_page.get_content()

    assert isinstance(previous_contents, ContentPageModel)
