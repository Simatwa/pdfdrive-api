from pydantic import HttpUrl

from pdfdrive_api.core.book.models import RecommendedBook


class ExtraRecommendedBook(RecommendedBook):
    cover_image: HttpUrl
