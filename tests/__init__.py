from pathlib import Path

recons_dir = Path(__file__).parent.parent / "recons"

book_path_content = open(recons_dir / "book.html").read()

index_path_content = open(recons_dir / "index.html").read()
