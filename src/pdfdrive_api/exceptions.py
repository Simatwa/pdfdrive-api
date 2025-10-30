class PdfDriveApiException(Exception):
    """Base exception"""


class NavigationError(PdfDriveApiException): ...
