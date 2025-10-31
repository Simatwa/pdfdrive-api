from json import loads

from pydantic import BaseModel, HttpUrl, field_validator


class PageMetadataModel(BaseModel):
    page_url: HttpUrl
    page_title: str
    page_image: HttpUrl | None
    page_description: str | None
    page_next: HttpUrl | None = None
    page_schema: dict  # | None = None

    @field_validator("page_schema", mode="before")
    def validate_page_schema(value: str | None):
        if value and isinstance(value, str):
            value = loads(value)

        return value


class BookPanelModel(BaseModel):
    title: str
    cover_image: HttpUrl
    rate: int
    url: str


class BooksGroupModel(BaseModel):
    name: str
    books: list[BookPanelModel]


class CurrentPageBooksModel(BooksGroupModel):
    current_page: int
    total_pages: int


class BooksCategoryModel(BaseModel):
    name: str
    url: HttpUrl


class ContentPageModel(BaseModel):
    books_category: list[BooksCategoryModel]
    search_placeholder: str
    books: CurrentPageBooksModel
    other_books: list[BooksGroupModel]
    metadata: PageMetadataModel

    def get_page_path(self, page_number: int) -> str:
        return f"/page/{page_number}"

    @property
    def has_next_page(self) -> bool:
        return self.books.current_page < self.books.total_pages

    @property
    def has_previous_page(self) -> bool:
        return self.books.current_page > 1

    @property
    def previous_page_path(self) -> str | None:
        if self.has_previous_page:
            return self.get_page_path(self.books.current_page - 1)

    @property
    def next_page_path(self) -> str | None:
        if self.has_next_page:
            return self.get_page_path(self.books.current_page + 1)

    @property
    def last_page_path(self) -> str:
        return self.get_page_path(self.books.total_pages)
