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
    NOVELS = "novels"
    SELF_IMPROVEMENT = "download-self-improvement-pdf"
    SIMILAR_FREE_EBOOKS = "download-similar-free-ebooks"
    BUSINESS_AND_CAREER = "14-download-business-career-pdf"
    GENERAL_KNOWLEDGE = "general-knowledge-books"
    BIOGRAPHY = "biography"
    ACADEMIC_AND_EDUCATION = "8-download-academic-education-pdf"
    FINANCIAL = "financial"
    HISTORY = "download-history-pdf"
    RELIGION = "19-download-religion-pdf"
    DOWNLOAD_SELF_IMPROVEMENT_PDF = "download-self-improvement-pdf"
    DOWNLOAD_SIMILAR_FREE_EBOOKS = "download-similar-free-ebooks"
    DOWNLOAD_BUSINESS_AND_CAREER_PDF = "14-download-business-career-pdf"
    DOWNLOAD_ACADEMIC_AND_EDUCATION_PDF = "8-download-academic-education-pdf"
    DOWNLOAD_HISTORY_PDF = "download-history-pdf"
    DOWNLOAD_RELIGION_PDF = "19-download-religion-pdf"
