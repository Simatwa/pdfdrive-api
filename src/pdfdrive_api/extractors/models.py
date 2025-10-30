from json import loads

from pydantic import BaseModel, HttpUrl, field_validator


class PageMetadataModel(BaseModel):
    page_url: HttpUrl
    page_title: str
    page_description: str
    page_next: HttpUrl  # | None = None
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


class HomepageModel(BaseModel):
    about: str
    sub_about: str
    books_category: list[BooksCategoryModel]
    search_placeholder: str
    page_books: CurrentPageBooksModel
    other_books: list[BooksGroupModel]
    metadata: PageMetadataModel
