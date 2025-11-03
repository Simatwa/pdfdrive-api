import re
from functools import cache

from pdfdrive_api.core.book.constants import name_short_map
from pdfdrive_api.core.book.models import (
    BookAboutModel,
    BookFAQ,
    BookPageModel,
    BookTag,
    DownloadBookPanelModel,
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

    def extract_panel_details(self) -> DownloadBookPanelModel:
        page_metadata = self.extract_page_metadata()

        title = self.page_content.find("h1", {"class": "main-box-title"}).get_text(
            strip=True
        )
        url = None

        download_url_nav = self.page_content.find(
            "a", {"class": "buttond downloadAPK dapk_b"}
        )

        if download_url_nav is not None:
            url = download_url_nav.get("href")

        rate = (
            self.page_content.find("span", {"class": "stars"})
            .get("style")
            .split(":")[1]
        )[:-1]

        return DownloadBookPanelModel(
            title=title,
            url=url,
            cover_image=page_metadata.page_image,
            rate=int(rate),
        )

    def extract_about(self) -> BookAboutModel:
        main = self.page_content.find("main", {"id": "main-site"})
        table_of_contents_soup = main.find("div", dict(id="rank-math-toc"))
        description = re.sub(
            r"\s{2,}",
            " ",
            (
                main.find("div", {"class": "entry-limit"})
                .find("p")
                .get_text()  # (strip=True)
            ),
        ).strip()

        table_of_content_items = [
            item.get_text(strip=True)
            for item in table_of_contents_soup.find_all("li")[:-1]
            if not re.match(r"#faq?-", item.find("a").get("href"))
        ]
        long_description = str(main.find("div", {"id": "descripcion"}))

        faq_soup = main.find("div", {"id": "rank-math-faq"})
        faq_items = []

        for entry in faq_soup.find_all("div", {"class": "rank-math-list-item"}):
            question = entry.find("h3", {"class": "rank-math-question"}).get_text(
                strip=True
            )
            answer = entry.find("div", {"class": "rank-math-answer"}).get_text(
                strip=True
            )
            faq_items.append(BookFAQ(question=question, answer=answer))

        return BookAboutModel(
            description=description,
            table_of_contents=table_of_content_items,
            long_description=long_description,
            faqs=faq_items,
        )

    def extract_metadata(self) -> MetadataModel:
        table_soup = self.page_content.find("div", dict(id="descripcion")).find(
            "table"
        )

        table_rows = table_soup.find_all("tr")
        amazon_link_soup = table_rows[-1].find("a")
        metadata_items = {}

        if amazon_link_soup:
            metadata_items.update({"amazon_link": amazon_link_soup.get("href")})

            for row_soup in table_rows[:-1]:
                try:
                    # print(row_soup)
                    table_header = row_soup.find("th").get_text(strip=True)
                    table_data_soup = row_soup.find("td")

                    if table_data_soup is not None:
                        table_data = table_data_soup.get_text()

                    else:
                        table_data = row_soup.find_all("th")[-1].get_text(strip=True)

                    metadata_key = name_short_map.get(
                        table_header, table_header.lower()
                    )

                    metadata_items[metadata_key] = table_data

                except Exception:
                    pass

            return MetadataModel(**metadata_items)

        else:
            for row_soup in table_rows:
                ths = row_soup.find_all("th")

                if not len(ths):
                    ths = row_soup.find_all("td")

                table_header = ths[0].get_text(strip=True)
                table_data = ths[1].get_text(strip=True)

                amazon_link_soup = ths[1].find(
                    "a", {"rel": "noreferrer noopener sponsored"}
                )

                if amazon_link_soup:
                    metadata_items["amazon_link"] = amazon_link_soup.get("href")

                metadata_key = name_short_map.get(table_header, table_header.lower())

                metadata_items[metadata_key] = table_data

            return MetadataModel(**metadata_items)

    def extract_tags(self) -> list[BookTag]:
        tags_soup = self.page_content.find("div", dict(id="tags"))

        if not tags_soup:
            return []

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
