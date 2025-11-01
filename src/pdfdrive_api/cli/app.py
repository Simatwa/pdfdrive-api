from cyclopts import App

from pdfdrive_api.cli.commands.download import Download
from pdfdrive_api.cli.commands.search import Search

app = App(
    help="Explore, search and download ebooks from pdfdrive.com.",
    version_flags=["-v", "--version"],
    result_action="",
)

app.command(Search)
app.command(Download)
