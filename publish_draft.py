import argparse
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument("article")
args = parser.parse_args()

def move_draft_to_srcs(article: str):
    srcs_path = pathlib.Path("./srcs")
    draft_path = pathlib.Path("./drafts")
    try:
        draft_article = draft_path / article
    except FileNotFoundError:
        print(f"No such file name in drafts directory: {article}")
    draft_article.rename(srcs_path / article)

move_draft_to_srcs(args.article)
