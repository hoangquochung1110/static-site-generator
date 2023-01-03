import pathlib
from simple_term_menu import TerminalMenu


root_path = pathlib.Path(__file__).parent
drafts_path = root_path / "drafts"
srcs_path = root_path / "srcs"


def menu():
    posts: pathlib.PosixPath = list(drafts_path.glob("*.md"))
    options = [post.name for post in posts]
    draft_menu = TerminalMenu(options)
    draft_menu._init_term()
    try:
        while True:
            menu_entry_index = draft_menu.show()
            move_draft_to_srcs(options[menu_entry_index])
    except KeyboardInterrupt:
        import sys
        sys.exit(0)

    
def move_draft_to_srcs(article: str):
    try:
        draft_article = drafts_path / article
    except FileNotFoundError:
        print(f"No such file name in drafts directory: {article}")
    draft_article.rename(srcs_path / draft_article.name)


if __name__ == "__main__":
    menu()
