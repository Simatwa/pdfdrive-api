from collections.abc import Iterable
from typing import Any

import rich
from rich.prompt import Prompt
from rich.table import Table

from pdfdrive_api import ContentPageModel


def display_page_results(content_page: ContentPageModel):
    table = Table(
        title=(
            f"{content_page.books.name} "
            f"(Pg. {content_page.books.current_page}/"
            f"{content_page.books.total_pages})"
        ),
        show_lines=True,
    )

    table.add_column("Index.", style="white", justify="center")
    table.add_column("Title", style="cyan")
    table.add_column("Rate")
    table.add_column("Url")

    for index, book in enumerate(content_page.books.books):
        table.add_row(str(index), book.title, f"{book.rate}%", book.url)

    rich.print(table)


def choose_one_item(
    items: Iterable, prompt="> Enter item index (click enter to skip)"
) -> Any | None:
    item_indexes = [""]

    for index in range(len(items)):
        item_indexes.append(str(index))

    item_index = Prompt.ask(prompt, choices=item_indexes)

    if item_index.isdigit():
        return items[int(item_index)]

    else:
        rich.print("\n>> Skipped ...", end="\r",)
