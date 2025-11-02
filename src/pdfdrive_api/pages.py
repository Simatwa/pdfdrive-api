import re
from typing import Literal

from pdfdrive_api.core.book.extractor import BookDetailsExtractor
from pdfdrive_api.core.book.models import BookPageModel
from pdfdrive_api.core.finder.extractor import PageListingExtractor
from pdfdrive_api.core.finder.models import ContentPageModel
from pdfdrive_api.exceptions import NavigationError
from pdfdrive_api.requests import Session
from pdfdrive_api.utils import is_url, slugify, validate_book_page_url


class BasePage:
    """Base page contents"""

    url: str = ""

    def __init__(self, page_number: int = None, session: Session = Session()):
        new_url = self._form_url_for_page(page_number)
        self.url = new_url
        self.session = session
        self.extractor: PageListingExtractor = None

    def _form_url_for_page(self, page_number: int | None) -> str:
        if page_number is None:
            return self.url

        current_url = self.url

        page_path_pattern = re.compile(r".*(?P<page_path>/page/\d+/?$)")
        page_path_match = page_path_pattern.match(current_url)

        if page_path_match is not None:
            page_path_ = page_path_match.groupdict()["page_path"]

            return re.sub(page_path_ + r"$", f"/page/{page_number}/", current_url)

        else:
            return (
                current_url
                + f"{'' if current_url.endswith('/') else '/'}page/{page_number}/"
            )

    def get_requests_params(self) -> dict:
        """Override this in subclass"""
        return {}

    async def update_page_contents(self, if_none: bool = False) -> None:
        if if_none and self.extractor is not None:
            return

        # print(self.url)
        resp = await self.session.get(self.url, params=self.get_requests_params())
        self.extractor = PageListingExtractor(resp.text)

    async def __aenter__(self):
        await self.update_page_contents()
        return self

    async def __aexit__(self, *args, **kwargs):
        self.extractor = None

    async def get_content(self, force_update: bool = False) -> ContentPageModel:
        await self.update_page_contents(if_none=force_update is False)
        return self.extractor.extract_page_content()

    def __set_nav_basepage(
        self,
        target_page_number: int,
        target_page_path: str,
        current_page_identity: Literal["last", "first"],
    ) -> "BasePage":
        if not target_page_path:
            raise NavigationError(
                f"You have reached the {current_page_identity} page of the "
                "search results"
            )

        # TODO: Fix this to duplicate class instead of modifying existing one

        next_base = self  # deepcopy(self)

        next_base.url = self._form_url_for_page(target_page_number)
        next_base.extractor = None

        return next_base

    async def next_page(self, current_page: ContentPageModel) -> "BasePage":
        return self.__set_nav_basepage(
            current_page.books.current_page + 1, current_page.next_page_path, "last"
        )

    async def previous_page(self, current_page: ContentPageModel) -> "BasePage":
        return self.__set_nav_basepage(
            current_page.books.current_page - 1,
            current_page.previous_page_path,
            "first",
        )


class HomePage(BasePage):
    """Landing page contents"""


class SearchPage(BasePage):
    """Provide book search functionality"""

    def __init__(
        self, query: str, page_number: int = None, session: Session = Session()
    ):
        super().__init__(page_number, session)
        self.query = query

    def get_requests_params(self):
        return {"s": self.query}


class CategoryPage(BasePage):
    def __init__(
        self, name: str, page_number: int = None, session: Session = Session()
    ):
        self.url = f"/category/{slugify(name)}/"
        super().__init__(page_number, session)


class TagPage(BasePage):
    def __init__(
        self, url_or_name: str, page_number: int = None, session: Session = Session()
    ):
        self.url = (
            f"/tag/{slugify(url_or_name)}/"
            if not is_url(url_or_name)
            else url_or_name
        )
        super().__init__(page_number, session)


class URLPage(BasePage):
    def __init__(
        self, url: str, page_number: int = None, session: Session = Session()
    ):
        self.url = url
        super().__init__(page_number, session)


class BookPage:
    """Specific book page details"""

    def __init__(self, url: str, session: Session = Session()):
        self.url = validate_book_page_url(url)
        self.session = session
        self.extractor: BookDetailsExtractor = None

    async def get_page_contents(self) -> str:
        resp = await self.session.get(self.url)

        page_content = resp.text
        self.extractor = BookDetailsExtractor(page_content)

        return page_content

    async def get_content(self) -> BookPageModel:
        await self.get_page_contents()
        return self.extractor.extract_page_content()
