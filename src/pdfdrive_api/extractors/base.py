from pdfdrive_api.extractors.models import (
    BookPanelModel,
    BooksCategoryModel,
    BooksGroupModel,
    CurrentPageBooksModel,
    HomepageModel,
    PageMetadataModel,
)
from pdfdrive_api.types import HtmlSoup


class BooksListing:
    @classmethod
    def get_books_sections(
        cls, page_content: HtmlSoup, current_page: bool = False
    ) -> list[HtmlSoup] | HtmlSoup:
        books_sections = (
            page_content.find("main", dict(id="main-site"))
            .find("div", {"class": "container"})
            .find("div", {"class": "sections"})
        )

        sections = books_sections.find_all("div", {"class": "section"})
        if current_page:
            return sections[0]
        return sections

    @classmethod
    def extract_books_section_details(
        cls, section: HtmlSoup, current_page: bool = False
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
                .split(":")[:-1]
            )
            book = BookPanelModel(
                title=title, cover_image=cover_image, rate=int(rate), url=url
            )
            book_items.append(book)

        if current_page:
            page_navs = section.find_all("ul", {"class": "pagination"})
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
    @classmethod
    def get_page_head(cls, page_content: HtmlSoup) -> HtmlSoup:
        return page_content.find("head")

    @classmethod
    def extract_page_metadata(cls, page_content: HtmlSoup) -> PageMetadataModel:
        head = cls.get_page_head(page_content)
        title = head.find("title").get_text(strip=True)
        url = head.find("meta", dict(property="og:url")).get_text(strip=True)
        description = head.find("meta", dict(name="description")).get_text(
            strip=True
        )
        next = "https:" + head.find("meta", dict(rel="next")).get_text(strip=True)
        schema = head.find("script", dict(type="application/ld+json")).get_text(
            strip=True
        )

        metadata = PageMetadataModel(
            page_url=url,
            page_title=title,
            page_description=description,
            page_next=next,
            page_schema=schema,
        )
        return metadata

    @classmethod
    def extract_books_categories(
        cls, page_content: HtmlSoup
    ) -> list[BooksCategoryModel]:
        wrapper = page_content.find("div", {"class": "wrapper-inside"})
        wrapper_menu = wrapper.find("ul", dict(id="menu-footer-menu"))
        categories = wrapper_menu.find("ul", {"class": "sub-menu"})

        books_category_items = []

        for category in categories.find_all("li"):
            link = category.find("a")
            books_category = BooksCategoryModel(
                name=link.get_text(strip=True), url=link.get("url")
            )
            books_category_items.append(books_category)

        return books_category_items


class PageListingExtractor(ExtractorUtils):
    @classmethod
    def get_page_about(cls, page_content: HtmlSoup) -> tuple[str, str]:
        subheader = page_content.find("div", dict(id="subheader"))
        subheader_container = subheader.find("div", {"class": "subcontainer"})
        about = subheader_container.find("h1").get_text(strip=True)
        sub_about = subheader_container.find("h2").get_text(strip=True)
        return about, sub_about

    @classmethod
    def get_book_search_placeholder(cls, page_content: HtmlSoup) -> str:
        search_box = page_content.find("div", dict(id="searchBox"))
        search_input = search_box.find("input", dict(id="sbinput"))
        search_placeholder = search_input.get("placeholder")
        return search_placeholder

    @classmethod
    def current_page_books(cls, page_content: HtmlSoup) -> CurrentPageBooksModel:
        current_page_books_section = cls.get_books_sections(
            page_content, current_page=True
        )
        return cls.extract_books_section_details(
            current_page_books_section, current_page=True
        )

    @classmethod
    def other_books(cls, page_content: HtmlSoup) -> list[BooksGroupModel]:
        sections = cls.get_books_sections(page_content)
        books_group_items = []
        for section in sections:
            group_model = cls.extract_books_section_details(section)
            books_group_items.append(group_model)
        return books_group_items

    @classmethod
    def extract_page_contents(cls, page_content: HtmlSoup) -> HomepageModel:
        page_metadata = cls.extract_page_metadata(page_content)
        books_category = cls.extract_books_categories(page_content)
        about, sub_about = cls.get_page_about(page_content)
        search_placeholder = cls.get_book_search_placeholder(page_content)
        current_page_books = cls.current_page_books(page_content)
        other_books = cls.other_books(page_content)

        return HomepageModel(
            about=about,
            sub_about=sub_about,
            books_category=books_category,
            search_placeholder=search_placeholder,
            page_books=current_page_books,
            other_books=other_books,
            metadata=page_metadata,
        )
