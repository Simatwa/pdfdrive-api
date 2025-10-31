from typing import Literal

from pdfdrive_api.core.book.extractor import BookDetailsExtractor
from pdfdrive_api.core.book.models import BookPageModel
from pdfdrive_api.core.finder.extractor import PageListingExtractor
from pdfdrive_api.core.finder.models import ContentPageModel
from pdfdrive_api.exceptions import NavigationError
from pdfdrive_api.requests import Session
from pdfdrive_api.utils import slugify


class BasePage:
    """Base page contents"""

    url: str = ""

    def __init__(self, session: Session = Session()):
        self.session = session
        self.extractor: PageListingExtractor = None

    def get_requests_params(self) -> dict:
        """Override this in subclass"""
        return {}

    async def update_page_contents(self, if_none: bool = False) -> None:
        if if_none and self.extractor is not None:
            return

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
        self, target_page_path: str, current_page_identity: Literal["last", "first"]
    ) -> BasePage:
        if not target_page_path:
            raise NavigationError(
                f"You have reached the {current_page_identity} page of the search"
            )

        # TODO: Fix this to replicate class instead of modifying existing one

        next_base = self  # deepcopy(self)

        current_url = next_base.url

        new_url = None

        if "/page/" in current_url:
            new_url = (
                current_url[: -2 if current_url.endswith("/") else -1]
                + target_page_path[-2 if target_page_path.endswith("/") else -1]
            )

        else:
            new_url = current_url + target_page_path

        next_base.url = new_url + "/"
        next_base.extractor = None

        return next_base

    async def next_page(self, current_page: ContentPageModel) -> BasePage:
        return self.__set_nav_basepage(current_page.next_page_path, "last")

    async def previous_page(self, current_page: ContentPageModel) -> BasePage:
        return self.__set_nav_basepage(current_page.next_page_path, "first")


class Homepage(BasePage):
    """Landing page contents"""


class SearchPage(BasePage):
    """Provide book search functionality"""

    def __init__(self, query: str, session: Session = Session()):
        super().__init__(session)
        self.query = query

    def get_requests_params(self):
        return {"s": self.query}


class CategoryPage(BasePage):
    def __init__(self, name: str, session: Session = Session()):
        super().__init__(session)
        self.url = f"/category/{slugify(name)}/"


class TagPage(BasePage):
    def __init__(self, url_or_name: str, session: Session = Session()):
        self.url = (
            f"/tag/{slugify(url_or_name)}/"
            if not url_or_name.startswith("http")
            else url_or_name
        )
        super().__init__(session)


class URLPage(BasePage):
    def __init__(self, url: str, session: Session = Session()):
        self.url = url
        super().__init__(session)


class BookPage:
    """Specific book page details"""

    def __init__(self, url: str, session: Session = Session()):
        self.url = url
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
