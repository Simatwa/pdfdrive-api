from cyclopts import App

from pdfdrive_api.cli.commands.search import Search

app = App(help="Explore, search and download ebooks from pdfdrive.com.")

app.command(Search)
