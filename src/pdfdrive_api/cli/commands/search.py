from typing import Annotated

from cyclopts import Argument, Group, Parameter, validators

from pdfdrive_api import SearchPage
from pdfdrive_api.cli.commands.utils import (
    choose_one_item,
    display_page_results,
    prepare_start,
)
from pdfdrive_api.core.finder.models import BookPanelModel

quiet_select_one_group = Group(
    name="prompt-control",
    help="Controls user interaction",
    validator=validators.MutuallyExclusive(),
    # show_default=False - Showing "[default: False]" isn't too meaningful
    # for mutually-exclusive options.
    # negative="" - Don't create a "--no-" flag
    default_parameter=Parameter(show_default=False, negative=""),
)


async def Search(
    query: Annotated[str, Argument()],
    limit: Annotated[
        int,
        Parameter(
            name=[
                "--limit",
                "-l",
            ],
            validator=validators.Number(gt=0),
        ),
    ] = 1,
    select_one: Annotated[
        bool, Parameter(name=["--select-one", "-s"], group=quiet_select_one_group)
    ] = False,
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
            group=quiet_select_one_group,
        ),
    ] = False,
) -> BookPanelModel | None:
    """Search for a particular book by its title

    Args:
        query (Annotated[str, Parameter, optional): Search text.
        limit (Annotated[ int, Parameter, optional): Search page navigation limit.
        select_one (Annotated[bool, Parameter, optional): Prompt user to select book.
        yes (Annotated[bool, Parameter, optional): Proceed with the first book of the search results.
        quiet (Annotated[bool, Parameter, optional): Instead of prompting, proceed with book having same title as query.

    Returns:
        BookPanelModel | None
    """  # noqa: E501
    prepare_start(quiet=quiet)
    search = SearchPage(query)

    for x in range(limit):
        search_results = await search.get_content()

        books = search_results.books.books

        if yes:
            return books[0]

        if quiet:
            search_query = query.lower().strip()

            for book in books:
                if book.title.lower().strip() == search_query:
                    return book

        else:
            display_page_results(search_results)

        if select_one:
            choice = choose_one_item(books)
            if choice is not None:
                return choice

        search = await search.next_page(search_results)
