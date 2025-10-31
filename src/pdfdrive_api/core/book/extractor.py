from functools import cache

from pdfdrive_api.core.book.models import (
    BookAboutModel,
    BookPageModel,
    BookPanelModel,
    BookTag,
    MetadataModel,
    PageMetadataModel,
    RecommendedBook,
    RelatedBook,
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

    def extract_panel_details(self) -> BookPanelModel:
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
            .split(":")[1]
        )[:-1]

        return BookPanelModel(
            title=title,
            url=url,
            cover_image=page_metadata.page_image,
            rate=int(rate),
        )

    def extract_about(self) -> BookAboutModel:
        main = self.page_content.find("main", {"id": "main-site"})
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

    def extract_metadata(self) -> MetadataModel:
        name_short_map = {"Name of PDF": "name", "No Pages": "total_pages"}

        table_soup = self.page_content.find("div", dict(id="descripcion")).find(
            "table"
        )

        table_rows = table_soup.find_all("tr")
        amazon_link_row = table_rows[-1]

        metadata_items = {"amazon_link": amazon_link_row.find("a").get("href")}

        for row_soup in table_rows[:-1]:
            table_header = row_soup.find("th").get_text(strip=True)
            table_data = row_soup.find("td").get_text(strip=True)

            metadata_key = name_short_map.get(table_header, table_header.lower())

            metadata_items[metadata_key] = table_data

        return MetadataModel(**metadata_items)

    def extract_tags(self) -> list[BookTag]:
        tags_soup = self.page_content.find("div", dict(id="tags"))

        tag_items = []

        for tag in tags_soup.find_all("a"):
            name = tag.get_text(strip=True)
            link = tag.get("href")

            tag_items.append(BookTag(name=name, url=link))

        return tag_items

    def extract_related(self) -> list[RelatedBook]:
        related_soup = self.page_content.find("div", {"class": "box rlat"})
        related_items = []

        for related_soup in related_soup.find_all("div", {"class": "bav bav1"}):
            link_soup = related_soup.find("a")

            url = link_soup.get("href")
            title = link_soup.get("title")

            rate = (
                related_soup.find("span", {"class": "stars"})
                .get("style")
                .split(":")[1]
            )[:-1]
            image = related_soup.find("img").get("src")

            related_items.append(
                RelatedBook(title=title, cover_image=image, rate=rate, url=url)
            )

        return related_items

    def extract_recommended(self) -> list[RecommendedBook]:
        recommended_soup = self.page_content.find(
            "ul", {"class": "wp-block-latest-posts__list wp-block-latest-posts"}
        )

        recommended_items = []

        for link in recommended_soup.find_all("a"):
            title = link.get_text(strip=True)
            url = link.get("href")

            recommended_items.append(RecommendedBook(title=title, url=url))

        return recommended_items

    def extract_page_content(self) -> BookPageModel:
        return BookPageModel(
            page_metadata=self.extract_page_metadata(),
            book=self.extract_panel_details(),
            about=self.extract_about(),
            metadata=self.extract_metadata(),
            tags=self.extract_tags(),
            related=self.extract_related(),
            recommended=self.extract_recommended(),
        )
