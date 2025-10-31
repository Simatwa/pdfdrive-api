from bs4 import BeautifulSoup
from bs4.element import Tag

from pdfdrive_api.core.finder.models import (
    BookPanelModel,
    BooksCategoryModel,
    BooksGroupModel,
    ContentPageModel,
    CurrentPageBooksModel,
    PageMetadataModel,
)
from pdfdrive_api.types import HtmlSoup
from pdfdrive_api.utils import souper


class BooksListing:
    def __init__(self, page_content: HtmlSoup):
        self.page_content = souper(page_content)

    def get_books_sections(
        self, current_page: bool = False
    ) -> list[HtmlSoup] | HtmlSoup:
        books_section = self.page_content.find("main", {"id": "main-site"})
        section_items = []

        for section in books_section.find_all("div", {"class": "section"}):
            if section.find("div", {"class": "pagination-wrap"}):
                if current_page:
                    return section
                continue

            if not current_page:
                section_items.append(section)

        return section_items

    def extract_books_section_details(
        self, section: HtmlSoup, current_page: bool = False
    ) -> BooksGroupModel | CurrentPageBooksModel:
        name = section.find("div", {"class": "title-section"}).get_text(strip=True)

        book_items = []

        for book_panel in section.find_all("div", {"class": "bav bav1"}):
            link = book_panel.find("a")

            title = link.get_text(strip=True)
            url = link.get("href")

            cover_image = "https:" + book_panel.find("img").get("data-lazy-src")

            rate = (
                book_panel.find("span", {"class": "stars"})
                .get("style")
                .split(":")[1]
            )[:-1]

            book = BookPanelModel(
                title=title, cover_image=cover_image, rate=int(rate), url=url
            )
            book_items.append(book)

        if current_page:
            page_navs = section.find("ul", {"class": "pagination"}).find_all("li")
            last_page_nav = page_navs[-1]

            if "next" in last_page_nav.get_text(strip=True).lower():
                current_page_nav = page_navs[0]
                total_page_nav = page_navs[-2]

            else:
                current_page_nav = total_page_nav = page_navs[-1]

            current_page = current_page_nav.get_text(strip=True)

            total_pages = total_page_nav.get_text(strip=True)
            return CurrentPageBooksModel(
                name=name,
                books=book_items,
                current_page=int(current_page),
                total_pages=int(total_pages),
            )

        books_group = BooksGroupModel(name=name, books=book_items)

        return books_group


class ExtractorUtils(BooksListing):
    def get_page_head(self) -> HtmlSoup:
        return self.page_content.find("head")

    def extract_page_metadata(self) -> PageMetadataModel:
        head: HtmlSoup = self.get_page_head()
        title = head.find("title").get_text(strip=True)

        url = head.find("meta", dict(property="og:url")).get("content")
        image_soup = head.find("meta", dict(property="og:image"))

        image = None

        if image_soup:
            image = image_soup.get("content")

        description = head.find("meta", dict(name="description")).get("content")
        next_soup = head.find("meta", dict(rel="next"))
        next = None

        if next_soup:
            next = "https:" + next_soup.get("content")

        schema = head.find("script", dict(type="application/ld+json")).get_text(
            strip=True
        )

        metadata = PageMetadataModel(
            page_url=url,
            page_title=title,
            page_image=image,
            page_description=description,
            page_next=next,
            page_schema=schema,
        )
        return metadata

    def extract_books_categories(
        self,
    ) -> list[BooksCategoryModel]:
        wrapper = self.page_content.find("div", {"class": "wrapper-inside"})
        wrapper_menu = wrapper.find("ul", dict(id="menu-footer-menu"))
        categories = wrapper_menu.find("ul", {"class": "sub-menu"})

        books_category_items = []

        for category in categories.find_all("li"):
            link = category.find("a")

            books_category = BooksCategoryModel(
                name=link.get_text(strip=True), url=link.get("href")
            )

            books_category_items.append(books_category)

        return books_category_items


class PageListingExtractor(ExtractorUtils):
    def get_page_about(
        self,
    ) -> tuple[str, str]:
        subheader = self.page_content.find("div", dict(id="subheader"))
        subheader_container = subheader.find("div", {"class": "subcontainer"})

        about = subheader_container.find("h1").get_text(strip=True)
        sub_about = subheader_container.find("h2").get_text(strip=True)

        return about, sub_about

    def get_book_search_placeholder(
        self,
    ) -> str:
        search_box = self.page_content.find("div", dict(id="searchBox"))

        search_input = search_box.find("input", dict(id="sbinput"))
        search_placeholder = search_input.get("placeholder")
        return search_placeholder

    def current_page_books(
        self,
    ) -> CurrentPageBooksModel:
        current_page_books_section = self.get_books_sections(current_page=True)
        return self.extract_books_section_details(
            current_page_books_section, current_page=True
        )

    def other_books(
        self,
    ) -> list[BooksGroupModel]:
        sections = self.get_books_sections()
        books_group_items = []

        for index, section in enumerate(sections):
            group_model = self.extract_books_section_details(section)
            books_group_items.append(group_model)

        return books_group_items

    def extract_page_content(self) -> ContentPageModel:
        page_metadata = self.extract_page_metadata()
        books_category = self.extract_books_categories()
        about, sub_about = self.get_page_about()

        search_placeholder = self.get_book_search_placeholder()
        current_page_books = self.current_page_books()
        other_books = self.other_books()

        return ContentPageModel(
            about=about,
            sub_about=sub_about,
            books_category=books_category,
            search_placeholder=search_placeholder,
            books=current_page_books,
            other_books=other_books,
            metadata=page_metadata,
        )
