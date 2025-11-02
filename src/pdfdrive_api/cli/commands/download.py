from pathlib import Path
from typing import Annotated

from cyclopts import Argument, Parameter, validators
from cyclopts.types import URL

from pdfdrive_api import BookDetails
from pdfdrive_api.cli.commands.search import Search
from pdfdrive_api.download import DownloadedFile, Downloader
from pdfdrive_api.utils import is_url, validate_book_page_url


def _validate_filename(type_, value):
    if value is not None and "/" in value:
        raise ValueError(
            "value must not reference directory. Use --dir flag for that."
        )


async def Download(
    query: Annotated[
        URL | str,
        Argument(
            parameter=Parameter(
                validator=lambda type_, value: validate_book_page_url(value)
            )
        ),
    ],
    dir: Annotated[
        Path,
        Parameter(
            name=["--dir", "-d"],
            validator=validators.Path(exists=True, file_okay=False),
        ),
    ] = Path.cwd(),
    filename: Annotated[
        str | None,
        Parameter(name=["--filename", "-f"], validator=_validate_filename),
    ] = None,
    connections: Annotated[int, Parameter(validator=validators.Number(gt=0))] = 5,
    yes: Annotated[
        bool,
        Parameter(
            name=[
                "--yes",
                "-y",
            ]
        ),
    ] = False,
    quiet: Annotated[
        bool,
        Parameter(
            name=[
                "--quiet",
                "-q",
            ],
        ),
    ] = False,
) -> DownloadedFile:
    """Download ebook by specifying its title or page url

    Args:
        query (Annotated[str, Argument): Search text or book page url.
        dir (Annotated[Path, Parameter, optional): Directory for saving the downloaded file to.
        filename (Annotated[str  |  None, Parameter, optional): Downloaded ebook filename.
        connections (Annotated[int, Parameter, optional): Number of connections to use for download.
        yes (Annotated[ bool, Parameter, optional): Proceed with the first item of search results.
        quiet (Annotated[ bool, Parameter, optional): Proceed with ebook whose title match the query.
    """  # noqa: E501

    if is_url(query):
        book_details = await BookDetails(query).get_details(for_download=True)

    else:
        # perform search to get book & its details
        book = await Search(query, limit=1000, select_one=True, yes=yes, quiet=quiet)
        book_details = await BookDetails(book.url).get_details(for_download=True)

    download_url = book_details.book.download_url

    downloader = Downloader(dir=dir, part_dir=dir, tasks=connections)

    downloaded_file = await downloader.run(
        download_url, filename=filename, suppress_incompatible_error=True
    )

    return downloaded_file
