from pdfdrive_api.models import ExtraRecommendedBook
from pdfdrive_api.requests import Session
from pdfdrive_api.types import Html
from pdfdrive_api.utils import souper


class Extras:
    recommend_path = "/wp-admin/admin-ajax.php"

    def __init__(self, session: Session = Session()):
        self.session = session

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
