import argparse
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument("article")
args = parser.parse_args()

def move_draft_to_srcs(article: str):
    srcs_path = pathlib.Path("./srcs")
    root_path = pathlib.Path(".")
    try:
        draft_article = root_path / article
    except FileNotFoundError:
        print(f"No such file name in drafts directory: {article}")
    draft_article.rename(srcs_path / draft_article.name)

move_draft_to_srcs(args.article)
# TODO: auto build after moving to /srcs/