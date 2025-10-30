from pydantic import BaseModel, HttpUrl

from pdfdrive_api.core.finder.models import BookPanelModel, PageMetadataModel


class BookAboutModel(BaseModel):
    description: str
    table_of_contents: list[str]
    long_description: str


class MetadataModel(BaseModel):
    name: str
    total_pages: int
    author: str
    published: str
    language: str
    genres: str
    size: str
    amazon_link: HttpUrl


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
    book: BookPanelModel
    about: BookAboutModel
    metadata: MetadataModel
    tags: list[BookTag]
    related: list[RelatedBook]
    recommended: list[RecommendedBook]

    @property
    def download_url(self) -> str:
        return str(self.book.url)
