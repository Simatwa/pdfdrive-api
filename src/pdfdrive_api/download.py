from throttlebuster import (
    DownloadedFile,
    DownloadMode,
    DownloadTracker,
    ThrottleBuster,
)


class Downloader(ThrottleBuster):
    """Pdf downloader"""


__all__ = [
    "DownloadedFile",
    "DownloadMode",
    "DownloadTracker",
]
