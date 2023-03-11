import pathlib
import sys

from simple_term_menu import TerminalMenu

SOURCES = "srcs"
DRAFTS = "drafts"
TIL = "til"


def menu():
    """Populate terminal menu to pick a draft

    and move to destination.
    """
    root_path = pathlib.Path(__file__).parent
    drafts_path = root_path / DRAFTS
    srcs_path = root_path / SOURCES
    til_path = root_path / SOURCES / TIL
    posts = list(drafts_path.glob("*.md"))
    options = [post.name for post in posts]
    destinations = [SOURCES, TIL]
    draft_menu = TerminalMenu(options)
    selected_index = draft_menu.show()

    if selected_index is None:
        sys.exit(0)

    destination_menu = TerminalMenu(destinations)
    selected_dest_index = destination_menu.show()
    if selected_dest_index is None:
        sys.exit(0)

    if destinations[selected_dest_index] == SOURCES:
        dest_dir = srcs_path
    else:
        dest_dir = til_path

    move_draft_to_dest(options[selected_index], drafts_path, dest_dir)

def move_draft_to_dest(article: str, drafts_dir: pathlib.Path, dest_dir: pathlib.Path):
    draft_article = drafts_dir / article
    draft_article.rename(dest_dir / draft_article.name)

if __name__ == "__main__":
    menu()
