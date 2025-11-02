from cyclopts import App
from rich import print

from pdfdrive_api.cli.commands.download import Download
from pdfdrive_api.cli.commands.explore import Explore
from pdfdrive_api.cli.commands.search import Search

app_ = App(
    help="Explore, search and download ebooks from [cyan]pdfdrive.com.co[/cyan]",
    version_flags=["-v", "--version"],
    result_action=lambda _: None,
    help_format="rich",
)

app_.command(Search)
app_.command(Download)
app_.command(Explore)


def app():
    try:
        app_()

    except Exception as e:
        print(f">> ({e.__class__.__name__}): [yellow]{e}[/yellow]")

        from sys import exit

        exit(1)
