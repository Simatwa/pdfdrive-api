from pydantic import BaseModel, HttpUrl, field_validator

from pdfdrive_api.core.finder.models import BookPanelModel, PageMetadataModel


class DownloadBookPanelModel(BookPanelModel):
    url: HttpUrl | None = None

    @property
    def download_url(self) -> str:
        return str(self.url)


class BookFAQ(BaseModel):
    question: str
    answer: str


class BookAboutModel(BaseModel):
    description: str
    table_of_contents: list[str]
    long_description: str
    faqs: list[BookFAQ]


class MetadataModel(BaseModel):
    file_type: str | None = None
    total_pages: int | None = None
    author: str | None = None
    published: str | None = None
    language: str | None = None
    genres: str | None = None
    source: str | None = None
    size: str | None = None
    amazon_link: HttpUrl | None = None

    @field_validator("language")
    def validate_language(value: str | None):
        if value and value.lower().strip() == "enlgish":
            return "English"

        return value


class RelatedBook(BaseModel):
    title: str
    cover_image: HttpUrl | str
    rate: int
    url: HttpUrl | str


class RecommendedBook(BaseModel):
    title: str
    url: HttpUrl


class BookTag(BaseModel):
    name: str
    url: HttpUrl


class BookPageModel(BaseModel):
    page_metadata: PageMetadataModel
    book: DownloadBookPanelModel
    about: BookAboutModel
    metadata: MetadataModel
    tags: list[BookTag]
    related: list[RelatedBook]
    recommended: list[RecommendedBook]

    @property
    def download_url(self) -> str:
        return str(self.book.url)
