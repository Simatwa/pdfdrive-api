from pdfdrive_api.core.book.extractor import BookDetailsExtractor
from pdfdrive_api.core.book.models import BookPageModel
from pdfdrive_api.models import ExtraRecommendedBook
from pdfdrive_api.requests import Session
from pdfdrive_api.types import Html
from pdfdrive_api.utils import souper


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

            recommended_items.append(
                ExtraRecommendedBook(
                    title=link.get_text(strip=True),
                    url=link.get("href"),
                    cover_image=img_soup.get("src"),
                )
            )

        return recommended_items

    async def recommend(self, search_text: str) -> list[ExtraRecommendedBook]:
        resp = await self.session.async_client.post(
            self.recommend_path,
            data={"action": "ajax_searchbox", "searchtext": search_text},
        )
        return self._extract_recommendations(resp.text)


class BookDetails:
    page_request_extra_params = {"download": "links", "opt": "1"}

    def __init__(self, book_page_url: str, session: Session = Session()):
        self.url = book_page_url
        self.session = session
        self.extractor: BookDetailsExtractor = None

    async def _update_details(self, force: bool = False) -> None:
        if self.extractor is not None and force is False:
            return

        contents = await self.session.get(
            self.url, params=self.page_request_extra_params
        )
        self.extractor = BookDetailsExtractor(contents)

    async def get_details(self, force_update: bool = False) -> BookPageModel:
        await self._update_details(force=force_update)
        return self.extractor.extract_page_content()
