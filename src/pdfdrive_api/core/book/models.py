from pydantic import BaseModel, HttpUrl

from pdfdrive_api.core.finder.models import BookPanelModel, PageMetadataModel


class DownloadBookPanelModel(BookPanelModel):
    @property
    def download_url(self) -> str:
        return str(self.url)


class BookAboutModel(BaseModel):
    description: str
    table_of_contents: list[str]
    long_description: str


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


class RelatedBook(BaseModel):
    title: str
    cover_image: HttpUrl
    rate: int
    url: HttpUrl


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
