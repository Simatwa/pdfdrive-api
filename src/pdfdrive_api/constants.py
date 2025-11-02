import re
from enum import StrEnum

BASE_URL = "https://pdfdrive.com.co/"

BOOK_PAGE_URL_PATTERN = re.compile(BASE_URL + r"[\w-]+", re.IGNORECASE)

REQUEST_HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": BASE_URL,
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0"
    ),
}


class BooksCategory(StrEnum):
    ASTROLOGY = "astrology"
    BIOGRAPHY = "biography"
    DOWNLOAD_BIOGRAPHY_PDF = "download-biography-pdf"
    ACADEMIC_AND_EDUCATION = "8-download-academic-education-pdf"
    BUSINESS_AND_CAREER = "14-download-business-career-pdf"
    HISTORY = "download-history-pdf"
    LAW = "download-law-pdf"
    RELIGION = "19-download-religion-pdf"
    SELF_IMPROVEMENT = "download-self-improvement-pdf"
    SIMILAR_FREE_EBOOKS = "download-similar-free-ebooks"
    # DOWNLOAD_SIMILAR_FREE_EBOOKS = "download-similar-free-ebooks"
    FINANCIAL = "financial"
    GAME = "game"
    GENERAL_KNOWLEDGE = "general-knowledge-books"
    HEALTH = "health"
    NOVELS = "novels"
    POETRY = "poetry"
    STOCK_MARKET_BOOK = "stock-market-book"
    UNCATEGORIZED = "uncategorized"
