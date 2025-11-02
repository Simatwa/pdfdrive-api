from typing import Annotated

from cyclopts import Group, Parameter, validators
from cyclopts.types import _url_validator
from rich import print
from rich.prompt import Confirm

from pdfdrive_api import (
    BookDetails,
    CategoryPage,
    HomePage,
    SearchPage,
    TagPage,
    URLPage,
)
from pdfdrive_api.cli.commands.utils import (
    choose_one_item,
    display_page_results,
    display_specific_book_details,
)
from pdfdrive_api.constants import BooksCategory

UserChoiceGroup = Group(
    name="search-criteria",
    help="Declare the exploration criteria",
    validator=validators.MutuallyExclusive(),
)

LimitControlGroup = Group(
    name="limit-control",
    help="Regulate the amount of pages to explore",
    validator=validators.MutuallyExclusive(),
    default_parameter=Parameter(show_default=True, negative="", required=False),
)


async def Explore(
    search: Annotated[
        str | None, Parameter(name=["--search", "-s"], group=UserChoiceGroup)
    ] = None,
    category: Annotated[
        BooksCategory | None,
        Parameter(name=["--category", "-c"], group=UserChoiceGroup),
    ] = None,
    tag: Annotated[
        str | None, Parameter(name=["--tag", "-t"], group=UserChoiceGroup)
    ] = None,
    url: Annotated[
        str | None,
        Parameter(
            name=["--url", "-u"], validator=_url_validator, group=UserChoiceGroup
        ),
    ] = None,
    homepage: Annotated[
        bool,
        Parameter(name=["--homepage", "-home"], group=UserChoiceGroup, negative=""),
    ] = True,
    limit: Annotated[
        int,
        Parameter(
            name=["--limit", "-l"],
            validator=validators.Number(gt=0),
            group=LimitControlGroup,
        ),
    ] = 10,
    offset: Annotated[
        int | None,
        Parameter(name=["--offset", "-o"], validator=validators.Number(gte=0)),
    ] = None,
    infinity: Annotated[
        bool, Parameter(name=["--infinity", "-i"], group=LimitControlGroup)
    ] = False,
    confirm: Annotated[bool, Parameter(name=["--confirm", "-m"])] = False,
    details: Annotated[bool, Parameter(name=["--details", "-d"])] = False,
):
    """Explore available ebooks by different criterias

    Args:
        search ( str, Parameter, optional): Explore books under a given search query
        category ( Annotated[ BooksCategory  |  None, Parameter, optional): Explore books under specific category.
        tag ( Annotated[ str, Parameter, optional): Explore books having a given particular tag.
        url ( Annotated[ str, Parameter, optional]): Page containing books listing to explore.
        homepage( Annoated[ bool, Parameter, optional]): Explore landing page contents.
        limit ( Annotated[ int, Parameter, optional): Number of pages to visit.
        offset ( Annotated[ int, Parameter, optional): Page numner for starting exploration from.
        infinity ( Annotated[ bool, Parameter, optional): Explore books without page limit.
        confirm ( Annotated[bool, Parameter, optional): Ask for permission to navigate to next page.
        details ( Annotated[bool, Parameter, optional): Ask for permission to show details of a particular book.
    """  # noqa: E501

    if search:
        target_page = SearchPage(query=search, page_number=offset)

    elif category:
        target_page = CategoryPage(name=category.value, page_number=offset)

    elif tag:
        target_page = TagPage(tag, page_number=offset)

    elif url:
        target_page = URLPage(url, page_number=offset)

    elif homepage:
        target_page = HomePage(page_number=offset)

    current_page_contents = await target_page.get_content()

    if infinity:
        limit = None

    while True:
        display_page_results(current_page_contents)

        if limit and current_page_contents.books.current_page >= limit:
            break

        if details:
            target_book = choose_one_item(current_page_contents.books.books)

            if target_book is not None:
                print(">> [yellow]Loading page contents ...[/yellow]", end="\r")

                book_details = await BookDetails(target_book.url).get_details()
                display_specific_book_details(book_details)

        if confirm:
            if not Confirm.ask(">> [yellow]Continue[/yellow] ...", default=infinity):
                print("> Quitting")
                break

        next_page = current_page_contents.books.current_page + 1

        display_limit = (
            limit
            if limit and limit <= current_page_contents.books.total_pages
            else current_page_contents.books.total_pages
        )

        print(
            f">> [yellow]Loading next page ({next_page}/{display_limit}) ...[/yellow]",
            end="\r",
        )

        target_page = await target_page.next_page(current_page_contents)

        current_page_contents = await target_page.get_content()
