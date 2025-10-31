import pytest

from pdfdrive_api.core.finder.models import ContentPageModel
from pdfdrive_api.pages import TagPage


@pytest.mark.asyncio
async def test_tag_page():
    search = TagPage("pdf-download")
    contents = await search.get_content()

    assert isinstance(contents, ContentPageModel)

    next_page = await search.next_page(contents)
    assert isinstance(next_page, TagPage)

    next_contents = await next_page.get_content()

    assert isinstance(next_contents, ContentPageModel)

    previous_page = await next_page.previous_page(next_contents)

    assert isinstance(previous_page, TagPage)

    previous_contents = await previous_page.get_content()

    assert isinstance(previous_contents, ContentPageModel)
