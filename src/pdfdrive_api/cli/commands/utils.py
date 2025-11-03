import logging
from collections.abc import Iterable
from typing import Any

import rich
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.table import Table

from pdfdrive_api import ContentPageModel
from pdfdrive_api.core.book.models import BookPageModel
from pdfdrive_api.utils import remove_tags


def display_page_results(content_page: ContentPageModel):
    table = Table(
        title=(
            f"{content_page.books.name} "
            f"(Pg. {content_page.books.current_page}/"
            f"{content_page.books.total_pages})"
        ),
        show_lines=True,
    )

    table.add_column("Index", style="white", justify="center")
    table.add_column("Title", style="cyan")
    table.add_column("Rate")
    table.add_column("Url")

    for index, book in enumerate(content_page.books.books):
        table.add_row(str(index), book.title, f"{book.rate}%", book.url)

    rich.print(table)


def display_specific_book_details(book_details: BookPageModel):
    d = book_details
    n = "\n"
    nn = n * 2

    details = f"""
<div align="center">

# [{d.book.title}]({d.book.url}) *(Rate : {d.book.rate})*

![Cover image]({d.book.cover_image})

</div>

# Metadata

| Header | Details |
|---------|---------|
| Url     | {d.book.url} |
| Author | {d.metadata.author} |
| Language | {d.metadata.language} |
| Published | {d.metadata.published} |
| Genres | {d.metadata.genres} |
| Number of pages | {d.metadata.total_pages} |
| File type | {d.metadata.file_type} |
| Size | {d.metadata.size} |
| Amazon link | [{d.metadata.amazon_link}]({d.metadata.amazon_link}) |
| Source | {d.metadata.source} |

---

# Short Description

{d.about.description}

# Table of Contents

{nn.join(d.about.table_of_contents)}

# Long Description

{remove_tags(d.about.long_description or "", nn)}

# FAQS

{
        nn.join(
            [
                f"{count}. {f.question}{nn}{f.answer}"
                for count, f in enumerate(d.about.faqs, start=1)
            ]
        )
    }

# Related Books

| No. | Title | | Cover Image | Rate |
| ---- | ----- | --- | -----  | ----- |
{
        "".join(
            [
                (
                    f"| {no} | [{book.title}]({book.url}) | "
                    f"![Cover image]({book.cover_image}) | {book.rate}%"
                )
                for no, book in enumerate(d.related, start=1)
            ]
        )
    }

# Recommended Books

| No.  | Title | Url |
| ---- | ----- | ---- |
{
        "".join(
            [
                f"| {no} | [{book.title}]({book.url}) | {book.url} |"
                for no, book in enumerate(d.recommended, start=1)
            ]
        )
    }

"""

    rich.print(Markdown(details))


def choose_one_item(
    items: Iterable, prompt="> Enter item index (click enter to skip)"
) -> Any | None:
    default_value = ""

    item_indexes = [default_value]

    for index in range(len(items)):
        item_indexes.append(str(index))

    item_index = Prompt.ask(prompt, choices=item_indexes, default=default_value)

    if item_index.isdigit():
        return items[int(item_index)]

    else:
        rich.print(
            "\n[yellow]>> Skipped (loading next page)...[/yellow]",
            end="\r",
        )


def prepare_start(quiet: bool = False, verbose: int = 0) -> None:
    """Set up some stuff for better CLI usage such as:

    - Set higher logging level for some packages.
    ...

    """
    if verbose > 3:
        verbose = 2
    logging.basicConfig(
        format=(
            "[%(asctime)s] : %(levelname)s - %(message)s"
            if verbose
            else "[%(module)s] %(message)s"
        ),
        datefmt="%d-%b-%Y %H:%M:%S",
        level=(
            logging.ERROR
            if quiet
            # just a hack to ensure
            #           -v -> INFO
            #           -vv -> DEBUG
            else (30 - (verbose * 10))
            if verbose > 0
            else logging.INFO
        ),
    )
    packages = ("httpx",)
    for package_name in packages:
        package_logger = logging.getLogger(package_name)
        package_logger.setLevel(logging.WARNING)
