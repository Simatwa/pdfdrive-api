from cyclopts import App

from pdfdrive_api.cli.commands.download import Download
from pdfdrive_api.cli.commands.explore import Explore
from pdfdrive_api.cli.commands.search import Search

app = App(
    help="Explore, search and download ebooks from [cyan]pdfdrive.com.co[/cyan]",
    version_flags=["-v", "--version"],
    result_action=lambda _: None,
    help_format="rich",
)

app.command(Search)
app.command(Download)
app.command(Explore)
