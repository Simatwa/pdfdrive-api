from functools import cache

from pdfdrive_api.core.book.models import (
    BookAboutModel,
    BookPanelModel,
    PageMetadataModel,
)
from pdfdrive_api.core.finder.extractor import ExtractorUtils
from pdfdrive_api.types import HtmlSoup
from pdfdrive_api.utils import souper


class BookDetailsExtractor:
    def __init__(self, page_content: HtmlSoup):
        self.page_content = souper(page_content)

    @cache
    def extract_page_metadata(self) -> PageMetadataModel:
        """NOTE: Caches response"""
        return ExtractorUtils(self.page_content).extract_page_metadata()

    def extract_book_details(self) -> BookPanelModel:
        page_metadata = self.extract_page_metadata()

        title = self.page_content.find("h1", {"class": "main-box-title"}).get_text(
            strip=True
        )

        url = self.page_content.find(
            "a", {"class": "buttond downloadAPK dapk_b"}
        ).get("href")

        rate = (
            self.page_content.find("span", {"class": "stars"})
            .get("style")
            .split(":")[:-1]
        )

        return BookPanelModel(
            title=title,
            url=url,
            cover_image=page_metadata.page_image,
            rate=int(rate),
        )

    def extract_book_about(self) -> BookAboutModel:
        main = self.page_content.find("div", {"id": "main-site"})
        table_of_contents_soup = main.find("div", dict(id="rank-math-toc"))
        description = main.find("div", {"class": "entry-limit"}).get_text(strip=True)
        table_of_content_items = [
            item.get_text(strip=True)
            for item in table_of_contents_soup.find_all("li")
        ]
        long_description = str(main.find("div", {"id": "descripcion"}))

        return BookAboutModel(
            description=description,
            table_of_contents=table_of_content_items,
            long_description=long_description,
        )
