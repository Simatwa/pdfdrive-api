from pdfdrive_api.core.book.extractor import BookDetailsExtractor
from pdfdrive_api.core.book.models import BookPageModel
from pdfdrive_api.models import ExtraRecommendedBook
from pdfdrive_api.requests import Session
from pdfdrive_api.types import Html
from pdfdrive_api.utils import souper, validate_book_page_url


class BaseSession:
    def __init__(self, session: Session = Session()):
        self.session = session


class Extras(BaseSession):
    recommend_path = "/wp-admin/admin-ajax.php"

    def _extract_recommendations(self, content: Html) -> list[ExtraRecommendedBook]:
        recommended_items = []

        for entry in souper(content).find_all("li"):
            link = entry.find("a")
            img_soup = entry.find("img")
            url = link.get("href")

            recommended_items.append(
                ExtraRecommendedBook(
                    title=link.get_text(strip=True),
                    url=url,
                    cover_image=img_soup.get("src"),
                )
            )

        return recommended_items

    async def recommend(self, search_text: str) -> list[ExtraRecommendedBook]:
        resp = await self.session.async_client.post(
            self.recommend_path,
            data={"action": "ajax_searchbox", "searchtext": search_text},
        )
        return self._extract_recommendations(str(resp.json()))


class BookDetails:
    page_request_extra_params = {"download": "links", "opt": "1"}

    def __init__(self, book_page_url: str, session: Session = Session()):
        self.url = validate_book_page_url(book_page_url)
        self.session = session
        self.extractor: BookDetailsExtractor = None

    async def _update_details(self, for_download: bool) -> None:
        contents = await self.session.get(
            self.url, params=(self.page_request_extra_params if for_download else {})
        )
        self.extractor = BookDetailsExtractor(contents)

    async def get_details(self, for_download: bool = False) -> BookPageModel:
        await self._update_details(for_download)
        return self.extractor.extract_page_content()

    async def get_details_for_download(self) -> BookPageModel:
        return await self.get_details(for_download=True)
