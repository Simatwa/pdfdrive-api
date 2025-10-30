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
    Novels = "novels"
    Self_Improvement = "download-self-improvement-pdf"
    Similar_Free_eBooks = "download-similar-free-ebooks"
    Business_and_Career = "14-download-business-career-pdf"
    General_Knowledge = "general-knowledge-books"
    Biography = "biography"
    Academic_and_Education = "8-download-academic-education-pdf"
    Financial = "financial"
    History = "download-history-pdf"
    Religion = "19-download-religion-pdf"
    Download_Self_Improvement_PDF = "download-self-improvement-pdf"
    Download_Similar_Free_eBooks = "download-similar-free-ebooks"
    Download_Business_and_Career_PDF = "14-download-business-career-pdf"
    Download_Academic_and_Education_PDF = "8-download-academic-education-pdf"
    Download_History_PDF = "download-history-pdf"
    Download_Religion_PDF = "19-download-religion-pdf"
