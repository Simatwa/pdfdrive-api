from enum import StrEnum

BASE_URL = "https://pdfdrive.com.co/"

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
    DOWNLOAD_ACADEMIC_AND_EDUCATION_PDF = "8-download-academic-education-pdf"
    BUSINESS_AND_CAREER = "14-download-business-career-pdf"
    DOWNLOAD_BUSINESS_AND_CAREER_PDF = "14-download-business-career-pdf"
    HISTORY = "download-history-pdf"
    DOWNLOAD_HISTORY_PDF = "download-history-pdf"
    LAW = "download-law-pdf"
    DOWNLOAD_LAW_PDF = "download-law-pdf"
    RELIGION = "19-download-religion-pdf"
    DOWNLOAD_RELIGION_PDF = "19-download-religion-pdf"
    SELF_IMPROVEMENT = "download-self-improvement-pdf"
    DOWNLOAD_SELF_IMPROVEMENT_PDF = "download-self-improvement-pdf"
    SIMILAR_FREE_EBOOKS = "download-similar-free-ebooks"
    DOWNLOAD_SIMILAR_FREE_EBOOKS = "download-similar-free-ebooks"
    FINANCIAL = "financial"
    GAME = "game"
    GENERAL_KNOWLEDGE = "general-knowledge-books"
    HEALTH = "health"
    NOVELS = "novels"
    POETRY = "poetry"
    STOCK_MARKET_BOOK = "stock-market-book"
    UNCATEGORIZED = "uncategorized"
